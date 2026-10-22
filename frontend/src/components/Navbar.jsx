/**
 * Navbar Bileşeni
 */

import { getUser, logout } from '../utils/auth';
import '../styles/Navbar.css';

function Navbar() {
  const user = getUser();

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="navbar-left">
          <h2>🎫 IT Helpdesk</h2>
        </div>
        <div className="navbar-right">
          <div className="user-info">
            <span className="user-name">{user?.full_name}</span>
            <span className="user-role">
              {user?.role === 'it_staff' ? '👨‍💻 IT Personeli' : '👤 Çalışan'}
            </span>
          </div>
          <button onClick={logout} className="logout-button">
            Çıkış
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
