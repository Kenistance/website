import React, { useEffect, useState } from 'react'
import TunnelGridBackground from '../components/TunnelGridBackground'
import CompletedProjectsHeader from '../components/CompletedProjectsHeader'
import styles from '../styles/Portfolio.module.css'

function Portfolio() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('https://website3-ho1y.onrender.com/api/portfolio/')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to load projects')
        return res.json()
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
    fetch('https://website3-ho1y.onrender.com/api/payments/stripe-checkout/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // include cookies/auth if required
      body: JSON.stringify({ project_id: project.id }),
    })
      .then((res) => {
        if (!res.ok) throw new Error('Could not create Stripe session')
        return res.json()
      })
      .then((data) => {
        // Stripe returns a checkout_url; redirect the user there
        if (data.checkout_url) {
          window.location.href = data.checkout_url
        } else {
          alert('Unable to start Stripe checkout')
        }
      })
      .catch((err) => {
        console.error('Stripe payment error:', err)
        alert('Error starting card payment: ' + err.message)
      })
  }

  // Start an Mpesa payment request
  function handleMpesaPayment(project) {
    const phone = prompt('Enter your Mpesa phone number (e.g. 2547XXXXXXXX)')
    if (!phone) return

    fetch('https://website3-ho1y.onrender.com/api/payments/mpesa-payment/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        project_id: project.id,
        phone_number: phone.trim(),
      }),
    })
      .then((res) => {
        if (!res.ok) throw new Error('Mpesa request failed')
        return res.json()
      })
      .then((data) => {
        // Assuming your backend returns a JSON response indicating success
        if (data.checkoutRequestID || data.response_code === '0') {
          alert('Mpesa payment prompt sent. Check your phone to complete payment.')
        } else {
          alert('Mpesa request response: ' + (data.errorMessage || JSON.stringify(data)))
        }
      })
      .catch((err) => {
        console.error('Mpesa payment error:', err)
        alert('Error initiating Mpesa payment: ' + err.message)
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
                        className={`${styles.paymentButton} ${styles.stripeButton}`}
                      >
                        Pay with Card
                        <span className={styles.priceText}>${project.price}</span>
                      </button>
                      <button
                        onClick={() => handleMpesaPayment(project)}
                        className={`${styles.paymentButton} ${styles.mpesaButton}`}
                      >
                        Pay with Mpesa
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