import { useState } from 'react'
import './Header.css'
import logo from './logo.png'

function Header() {

  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <img src={logo} />
        </div>
      </div>
    </header>
  )
}

export default Header
