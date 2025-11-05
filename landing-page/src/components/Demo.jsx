import './Demo.css'
import { useState, useEffect } from 'react'

function Demo() {
  const [progress, setProgress] = useState(0)
  const [currentMatch, setCurrentMatch] = useState('PSG vs. Marseille')
  const [scrapedCount, setScrapedCount] = useState(0)
  const [isActive, setIsActive] = useState(false)

  const matches = [
    'PSG vs. Marseille',
    'Lyon vs. Monaco',
    'Lakers vs. Warriors',
    'Real Madrid vs. Barcelona'
  ]

  useEffect(() => {
    if (isActive) {
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) {
            setIsActive(false)
            return 100
          }
          return prev + 2
        })

        if (progress % 25 === 0 && progress > 0) {
          setCurrentMatch(matches[Math.floor(progress / 25) % matches.length])
        }

        setScrapedCount(prev => Math.min(prev + 1, 15))
      }, 100)

      return () => clearInterval(interval)
    }
  }, [isActive, progress])

  const startScraping = () => {
    setProgress(0)
    setScrapedCount(0)
    setIsActive(true)
  }

  return (
    <section className="demo" id="demo">
      <div className="demo-container">
        <div className="demo-header">
          <h2 className="demo-title">
            See the
            <span className="demo-highlight"> Scraping in Action</span>
          </h2>
          <p className="demo-subtitle">
            Watch how the platform automatically collects and processes betting odds from multiple bookmakers
          </p>
        </div>

        <div className="demo-content">
          <div className="demo-sidebar">
            <div className="sidebar-title scraping-active">
              Scraping Filters
            </div>

            <div className="last-scraping-info">
              <span className="last-scraping-label">Last Scraping</span>
              <span className="last-scraping-date">2025-01-15 14:23:45</span>
            </div>

            <div className="aside-form">
              <div className="form-group">
                <label>Sport</label>
                <select>
                  <option>Football</option>
                </select>
              </div>

              <div className="form-group">
                <label>League</label>
                <select>
                  <option>Ligue 1</option>
                </select>
              </div>

              <button
                className="scraping-btn"
                onClick={startScraping}
                disabled={isActive}
              >
                {isActive ? 'Scraping...' : 'Launch Scraping'}
              </button>
            </div>

            {isActive && (
              <div className="scraping-progress">
                <div className="progress-header">
                  <h3>Scraping in Progress</h3>
                  <span className="progress-count">{scrapedCount}/15</span>
                </div>

                <div className="progress-bar-container">
                  <div className="progress-bar" style={{ width: `${progress}%` }}>
                    <span className="progress-percentage">{progress}%</span>
                  </div>
                </div>

                <div className="progress-info">
                  <div className="current-match">
                    <p><strong>Current:</strong> {currentMatch}</p>
                  </div>
                  <div className="bookmakers-info">
                    <p><strong>Bookmakers:</strong> {scrapedCount} scraped</p>
                  </div>
                </div>

                <div className="progress-message">
                  Extracting odds data from bookmaker websites...
                </div>
              </div>
            )}
          </div>

          <div className="demo-table-container">
            <h3 className="table-header">Scraped Data Results</h3>
            <table className="demo-table">
              <thead>
                <tr>
                  <th>Match</th>
                  <th>Home</th>
                  <th>Draw</th>
                  <th>Away</th>
                  <th>RTP</th>
                </tr>
              </thead>
              <tbody>
                <tr className="fade-in" style={{ animationDelay: '0s' }}>
                  <td className="match-name">PSG vs. Marseille</td>
                  <td className="odds">1.65</td>
                  <td className="odds">3.80</td>
                  <td className="odds">5.20</td>
                  <td className="trj trj-high">94.2%</td>
                </tr>
                <tr className="fade-in" style={{ animationDelay: '0.1s' }}>
                  <td className="match-name">Lyon vs. Monaco</td>
                  <td className="odds">2.10</td>
                  <td className="odds">3.40</td>
                  <td className="odds">3.50</td>
                  <td className="trj trj-high">92.8%</td>
                </tr>
                <tr className="fade-in" style={{ animationDelay: '0.2s' }}>
                  <td className="match-name">Lens vs. Nice</td>
                  <td className="odds">2.35</td>
                  <td className="odds">3.20</td>
                  <td className="odds">3.10</td>
                  <td className="trj trj-medium">91.5%</td>
                </tr>
                <tr className="fade-in" style={{ animationDelay: '0.3s' }}>
                  <td className="match-name">Rennes vs. Lille</td>
                  <td className="odds">2.50</td>
                  <td className="odds">3.30</td>
                  <td className="odds">2.90</td>
                  <td className="trj trj-medium">91.2%</td>
                </tr>
                <tr className="fade-in" style={{ animationDelay: '0.4s' }}>
                  <td className="match-name">Toulouse vs. Strasbourg</td>
                  <td className="odds">2.20</td>
                  <td className="odds">3.15</td>
                  <td className="odds">3.45</td>
                  <td className="trj trj-low">89.7%</td>
                </tr>
                <tr className="fade-in" style={{ animationDelay: '0.5s' }}>
                  <td className="match-name">Brest vs. Montpellier</td>
                  <td className="odds">1.95</td>
                  <td className="odds">3.50</td>
                  <td className="odds">4.00</td>
                  <td className="trj trj-high">93.5%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Demo
