import React, { useEffect, useState } from 'react'
import TunnelGridBackground from '../components/TunnelGridBackground'
import CompletedProjectsHeader from '../components/CompletedProjectsHeader'
import styles from '../styles/Portfolio.module.css'

function Portfolio() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [paymentLoading, setPaymentLoading] = useState(null) // Track which payment is processing

  // Helper function to get auth token (if you're using token auth)
  function getAuthToken() {
    // Return your auth token here - this depends on how you store it
    // For example, if using localStorage:
    // return localStorage.getItem('authToken')
    // Or if using cookies, the browser will handle it automatically with credentials: 'include'
    return localStorage.getItem('authToken') // Adjust based on your auth system
  }

  useEffect(() => {
    const authToken = getAuthToken();
    const headers = {};

    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`; // Adjust format based on your auth system (e.g., 'Token', 'Bearer')
    }

    fetch('https://website3-ho1y.onrender.com/api/portfolio/', {
      method: 'GET',
      headers: headers,
      credentials: 'include', // Important for sending cookies/session with the request
    })
      .then((res) => {
        if (!res.ok) {
          // Attempt to read error message from response body if available
          return res.json().catch(() => {
            throw new Error(`HTTP ${res.status}: Failed to load projects`);
          }).then(errorData => {
            throw new Error(errorData.detail || errorData.error || `HTTP ${res.status}: Failed to load projects`);
          });
        }
        return res.json();
      })
      .then((data) => {
        setProjects(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Error fetching projects:', err)
        setError(err.message)
        setLoading(false)
      })
  }, [])

  // Called when a project is free to download
  function handleFreeDownload(project) {
    if (project.download_link) {
      // Open the public URL in a new tab
      window.open(project.download_link, '_blank')
    } else {
      // Fallback: call your backend download endpoint
      window.location.href = `https://website3-ho1y.onrender.com/api/portfolio/${project.id}/download/`
    }
  }

  // Start a Stripe checkout session
  function handleStripePayment(project) {
    if (paymentLoading) return // Prevent multiple simultaneous requests
    
    setPaymentLoading(`stripe-${project.id}`)
    
    const authToken = getAuthToken()
    const headers = {
      'Content-Type': 'application/json',
    }
    
    // Add authorization header if token exists
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}` // Adjust format based on your auth system
    }

    fetch('https://website3-ho1y.onrender.com/api/payments/stripe-checkout/', {
      method: 'POST',
      headers: headers,
      credentials: 'include', // include cookies/auth
      body: JSON.stringify({ project_id: project.id }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then(errorData => {
            throw new Error(errorData.error || `HTTP ${res.status}: Could not create Stripe session`)
          })
        }
        return res.json()
      })
      .then((data) => {
        console.log('Stripe response:', data)
        // Check for success and checkout_url
        if (data.success && data.redirect_url) { // Changed to redirect_url based on views.py
          window.location.href = data.redirect_url
        } else if (data.checkout_url) { // Keep for backward compatibility if needed
          window.location.href = data.checkout_url
        } else {
          throw new Error(data.error || 'Unable to get checkout URL')
        }
      })
      .catch((err) => {
        console.error('Stripe payment error:', err)
        alert('Error starting card payment: ' + err.message)
      })
      .finally(() => {
        setPaymentLoading(null)
      })
  }

  // Validate phone number format
  function validatePhoneNumber(phone) {
    // Remove any spaces, dashes, or other characters
    const cleaned = phone.replace(/[\s\-\(\)]/g, '')
    
    // Check if it starts with 254 and has correct length
    if (cleaned.startsWith('254') && cleaned.length === 12) {
      return cleaned
    }
    
    // If it starts with 0, replace with 254
    if (cleaned.startsWith('0') && cleaned.length === 10) {
      return '254' + cleaned.substring(1)
    }
    
    // If it starts with 7 and has 9 digits, add 254
    if (cleaned.startsWith('7') && cleaned.length === 9) {
      return '254' + cleaned
    }
    
    return null
  }

  // Start an Mpesa payment request
  function handleMpesaPayment(project) {
    if (paymentLoading) return // Prevent multiple simultaneous requests
    
    const phoneInput = prompt('Enter your M-Pesa phone number:\n(Format: 0712345678 or 254712345678)')
    if (!phoneInput) return

    const validatedPhone = validatePhoneNumber(phoneInput.trim())
    if (!validatedPhone) {
      alert('Invalid phone number format. Please use format: 0712345678 or 254712345678')
      return
    }

    setPaymentLoading(`mpesa-${project.id}`)

    const authToken = getAuthToken()
    const headers = {
      'Content-Type': 'application/json',
    }
    
    // Add authorization header if token exists
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}` // Adjust format based on your auth system
    }

    fetch('https://website3-ho1y.onrender.com/api/payments/mpesa-payment/', {
      method: 'POST',
      headers: headers,
      credentials: 'include',
      body: JSON.stringify({
        project_id: project.id,
        phone_number: validatedPhone,
      }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then(errorData => {
            throw new Error(errorData.error || errorData.errorMessage || `HTTP ${res.status}: M-Pesa request failed`)
          })
        }
        return res.json()
      })
      .then((data) => {
        console.log('M-Pesa response:', data)
        
        if (data.success) {
          alert('M-Pesa payment prompt sent to your phone. Please check your phone and enter your M-Pesa PIN to complete the payment.')
        } else {
          // Show the specific error message from the backend
          const errorMsg = data.errorMessage || data.error || 'M-Pesa payment request failed'
          alert('M-Pesa Error: ' + errorMsg)
          console.error('M-Pesa error details:', data)
        }
      })
      .catch((err) => {
        console.error('M-Pesa payment error:', err)
        alert('Error initiating M-Pesa payment: ' + err.message)
      })
      .finally(() => {
        setPaymentLoading(null)
      })
  }

  if (loading) {
    return (
      <div className="relative min-h-screen bg-gradient-to-b from-black via-gray-900 to-black">
        <TunnelGridBackground />
        <div className="relative z-10 p-8 max-w-5xl mx-auto text-white">
          <CompletedProjectsHeader />
          <p className="text-lg animate-pulse">Loading projects...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="relative min-h-screen bg-gradient-to-b from-black via-gray-900 to-black">
        <TunnelGridBackground />
        <div className="relative z-10 p-8 max-w-5xl mx-auto text-white">
          <CompletedProjectsHeader />
          <p className="text-lg text-red-300">Error: {error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-black via-gray-900 to-black">
      <TunnelGridBackground />

      <div className="relative z-10 p-8 max-w-5xl mx-auto text-white">
        <CompletedProjectsHeader />

        {projects.length === 0 ? (
          <p className="text-lg text-red-300">No projects found.</p>
        ) : (
          <ul className={styles.projectList}>
            {projects.map((project) => (
              <li key={project.id} className={styles.projectItem}>
                <h2 className={styles.projectTitle}>{project.title}</h2>
                <p className={styles.projectDescription}>{project.description}</p>
                {project.image_url && (
                  <img
                    src={project.image_url}
                    alt={project.title}
                    className={styles.projectImage}
                  />
                )}

                {/* Styled payment buttons section */}
                <div className={styles.paymentContainer}>
                  {project.requires_payment ? (
                    <>
                      <button
                        onClick={() => handleStripePayment(project)}
                        disabled={paymentLoading === `stripe-${project.id}`}
                        className={`${styles.paymentButton} ${styles.stripeButton} ${
                          paymentLoading === `stripe-${project.id}` ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                      >
                        {paymentLoading === `stripe-${project.id}` ? 'Processing...' : 'Pay with Card'}
                        <span className={styles.priceText}>${project.price}</span>
                      </button>
                      <button
                        onClick={() => handleMpesaPayment(project)}
                        disabled={paymentLoading === `mpesa-${project.id}`}
                        className={`${styles.paymentButton} ${styles.mpesaButton} ${
                          paymentLoading === `mpesa-${project.id}` ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                      >
                        {paymentLoading === `mpesa-${project.id}` ? 'Processing...' : 'Pay with M-Pesa'}
                        <span className={styles.priceText}>${project.price}</span>
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={() => handleFreeDownload(project)}
                      className={`${styles.paymentButton} ${styles.downloadButton}`}
                    >
                      Download Free
                    </button>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default Portfolio