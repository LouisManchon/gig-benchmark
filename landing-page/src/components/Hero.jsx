import './Hero.css'

function Hero() {
  return (
    <section className="hero">
      <div className="hero-container">
        <div className="hero-content">
          <h1 className="hero-title">
            Automated Web Scraping
            <span className="hero-highlight"> & Odds Analysis Platform</span>
          </h1>
          <p className="hero-description">
            A full-stack web application featuring advanced web scraping technology to automatically collect and analyze sports betting odds from 15 bookmakers in real-time.
            Demonstrates automated data extraction, processing pipelines, and interactive visualization across Football, Basketball, Rugby, and Tennis.
          </p>
        </div>

        <div className="hero-image">
          <div className="dashboard-preview">
            <table className="preview-table">
              <thead>
                <tr>
                  <th>Bookmaker</th>
                  <th>Average TRJ <span>↕</span></th>
                  <th>Evolution <span>↕</span></th>
                </tr>
              </thead>
              <tbody>
                <tr className="animate-fade-in">
                  <td className='bookmaker'>Bet365</td>
                  <td className="rtp trj-low">92.5%</td>
                  <td>
                    <div className="evol-container">
                      <p className="previous-trj">
                        92.2% <span className="arrow-up">↑</span>
                      </p>
                    </div>
                  </td>
                </tr>
                <tr className="animate-fade-in" style={{ animationDelay: '0.1s' }}>
                  <td className='bookmaker'>Unibet</td>
                  <td className="rtp trj-low">91.8%</td>
                  <td>
                    <div className="evol-container">
                      <p className="previous-trj">
                        91.8% <span className="arrow-stable">→</span>
                      </p>
                    </div>
                  </td>
                </tr>
                <tr className="animate-fade-in" style={{ animationDelay: '0.2s' }}>
                  <td className='bookmaker'>Winamax</td>
                  <td className="rtp trj-high">90.2%</td>
                  <td>
                    <div className="evol-container">
                      <p className="previous-trj">
                        90.7% <span className="arrow-down">↓</span>
                      </p>
                    </div>
                  </td>
                </tr>
                <tr className="animate-fade-in" style={{ animationDelay: '0.2s' }}>
                  <td className='bookmaker'>ParionsSport</td>
                  <td className="rtp trj-high">91.2%</td>
                  <td>
                    <div className="evol-container">
                      <p className="previous-trj">
                        92.7% <span className="arrow-down">↓</span>
                      </p>
                    </div>
                  </td>
                </tr>                
                <tr className="animate-fade-in" style={{ animationDelay: '0.2s' }}>
                  <td className='bookmaker'>PMU</td>
                  <td className="rtp trj-low">89.4%</td>
                  <td>
                    <div className="evol-container">
                      <p className="previous-trj">
                        89.9% <span className="arrow-down">↓</span>
                      </p>
                    </div>
                  </td>
                </tr>
                <tr className="animate-fade-in" style={{ animationDelay: '0.2s' }}>
                  <td className='bookmaker'>GenyBet</td>
                  <td className="rtp trj-high">90.1%</td>
                  <td>
                    <div className="evol-container">
                      <p className="previous-trj">
                        90.7% <span className="arrow-down">↓</span>
                      </p>
                    </div>
                  </td>
                </tr>
                <tr className="animate-fade-in" style={{ animationDelay: '0.3s' }}>
                  <td className='bookmaker'>Bwin</td>
                  <td className="rtp trj-low">91.3%</td>
                  <td>
                    <div className="evol-container">
                      <p className="previous-trj">
                        91.1% <span className="arrow-up">↑</span>
                      </p>
                    </div>
                  </td>
                </tr>
                <tr className="animate-fade-in" style={{ animationDelay: '0.4s' }}>
                  <td className='bookmaker'>Betclic</td>
                  <td className="rtp trj-high">89.8%</td>
                  <td>
                    <div className="evol-container">
                      <p className="previous-trj">
                        90.4% <span className="arrow-down">↓</span>
                      </p>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero
