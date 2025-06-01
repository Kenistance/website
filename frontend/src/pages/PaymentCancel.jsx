function PaymentCancel() {
    return (
      <div className="min-h-screen flex items-center justify-center bg-red-50 text-red-800">
        <div>
          <h1 className="text-3xl font-bold">Payment Cancelled</h1>
          <p className="mt-2">You cancelled the payment. No charges were made.</p>
        </div>
      </div>
    )
  }
  
  export default PaymentCancel
  