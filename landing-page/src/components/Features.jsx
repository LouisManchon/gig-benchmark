import './Features.css'

function Features() {
  const features = [
    {
      title: 'Automated Web Scraping',
      description: 'Advanced scraping engine using Selenium and async requests to extract data from 15 bookmakers. Auto scraping every 6 hours is available.'
    },
    {
      title: 'Real-Time Data Pipeline',
      description: 'Automated data processing pipeline that collects, validates, and stores odds updates in real-time with MySQL database integration.'
    },
    {
      title: 'RTP Analysis Engine',
      description: 'Custom-built algorithm calculating Theoretical Return to Player (RTP) metrics across bookmakers to identify value and market inefficiencies.'
    },
    {
      title: 'Multi-Sport Coverage',
      description: 'Scalable scraping architecture supporting Football, Basketball, Rugby, and Tennis with sport-specific parsers and data normalization.'
    },
    {
      title: 'Evolution Tracking',
      description: 'Historical data storage and visualization showing odds movements over time with interactive charts powered by Chart.js.'
    },
    {
      title: 'Data Export & API',
      description: 'RESTful API endpoints and CSV export functionality for data access and integration with external analysis tools.'
    }
  ]

  return (
    <section className="features" id="features">
      <div className="features-container">
        <div className="features-header">
          <h2 className="features-title">
            Key Features
            <span className="features-highlight"> & Capabilities</span>
          </h2>
          <p className="features-subtitle">
            A comprehensive platform demonstrating full-stack development, data aggregation, and real-time analytics
          </p>
        </div>

        <div className="features-grid">
          {features.map((feature, index) => (
            <div
              key={index}
              className="feature-card"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Features
