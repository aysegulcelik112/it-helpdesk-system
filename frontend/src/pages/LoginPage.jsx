/**
 * Giriş Sayfası
 */

import { useState } from 'react';
import { authAPI } from '../services/api';
import { setToken, setUser } from '../utils/auth';
import { showToast } from '../utils/helpers';
import '../styles/LoginPage.css';

function LoginPage({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    department: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      if (isLogin) {
        response = await authAPI.login(formData.email, formData.password);
      } else {
        response = await authAPI.register(formData);
      }

      const { access_token, user } = response.data;
      setToken(access_token);
      setUser(user);
      onLogin(user);
      
      showToast(isLogin ? 'Giriş başarılı!' : 'Kayıt başarılı!', 'success');
      
      // Yönlendirme App.jsx'te otomatik olacak
      window.location.reload();
    } catch (error) {
      const message = error.response?.data?.detail || 'Bir hata oluştu';
      showToast(message, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>🎫 IT Destek Talep Sistemi</h1>
          <p>Şirket içi IT destek süreçlerini dijitalleştirin</p>
        </div>

        <div className="login-form-container">
          <div className="tab-buttons">
            <button 
              className={isLogin ? 'active' : ''} 
              onClick={() => setIsLogin(true)}
            >
              Giriş Yap
            </button>
            <button 
              className={!isLogin ? 'active' : ''} 
              onClick={() => setIsLogin(false)}
            >
              Kayıt Ol
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {!isLogin && (
              <>
                <div className="form-group">
                  <label>Ad Soyad</label>
                  <input
                    type="text"
                    value={formData.full_name}
                    onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                    required={!isLogin}
                    placeholder="Ahmet Yılmaz"
                  />
                </div>
                <div className="form-group">
                  <label>Departman</label>
                  <input
                    type="text"
                    value={formData.department}
                    onChange={(e) => setFormData({...formData, department: e.target.value})}
                    placeholder="Muhasebe"
                  />
                </div>
              </>
            )}

            <div className="form-group">
              <label>E-posta</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
                placeholder="ornek@company.com"
              />
            </div>

            <div className="form-group">
              <label>Şifre</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
                placeholder="••••••••"
                minLength={6}
              />
            </div>

            <button type="submit" className="submit-button" disabled={loading}>
              {loading ? 'İşlem yapılıyor...' : isLogin ? 'Giriş Yap' : 'Kayıt Ol'}
            </button>
          </form>

          <div className="demo-accounts">
            <p>Demo hesaplar:</p>
            <small>IT: admin@company.com / admin123</small>
            <small>Çalışan: user@company.com / user123</small>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
