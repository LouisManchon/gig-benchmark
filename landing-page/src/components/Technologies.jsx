import './Technologies.css'

function Technologies() {
  const technologies = [
    {
      name: 'Django',
      category: 'Backend'
    },
    {
      name: 'Docker',
      category: 'Environment'
    },    
    {
      name: 'Symfony',
      category: 'Web Framework'
    },
    {
      name: 'Nginx',
      category: 'Proxy'
    },
    {
      name: 'MySQL',
      category: 'Database'
    },
    {
      name: 'Python  / Selenium',
      category: 'Web Scraping'
    },
    {
      name: 'RabbitMQ',
      category: 'Scraping tasks'
    },    
    {
      name: 'Twig',
      category: 'Frontend'
    },
    {
      name: 'HTML/CSS',
      category: 'Frontend'
    },
    {
      name: 'JavaScript',
      category: 'Frontend'
    },
  ]

  return (
    <section className="technologies" id="technologies">
      <div className="technologies-container">
        <h2 className="technologies-title">
          Technologies Used
        </h2>
        <p className="technologies-subtitle">
          This project was built using modern web technologies and frameworks
        </p>

        <div className="technologies-grid">
          {technologies.map((tech, index) => (
            <div
              key={index}
              className="tech-card"
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <div className="tech-name">{tech.name}</div>
              <div className="tech-category">{tech.category}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Technologies
