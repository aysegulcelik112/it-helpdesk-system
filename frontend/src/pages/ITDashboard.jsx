/**
 * IT Personeli Dashboard
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ticketsAPI } from '../services/api';
import { showToast, formatDate, getStatusColor, getPriorityColor } from '../utils/helpers';
import Navbar from '../components/Navbar';
import StatsSection from '../components/StatsSection';
import '../styles/Dashboard.css';

function ITDashboard() {
  const navigate = useNavigate();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    status: '',
    category: '',
    priority: '',
    search: ''
  });

  useEffect(() => {
    loadTickets();
  }, [filters.status, filters.category, filters.priority]);

  const loadTickets = async () => {
    try {
      const response = await ticketsAPI.list({
        status: filters.status,
        category: filters.category,
        priority: filters.priority
      });
      setTickets(response.data);
    } catch (error) {
      showToast('Talepler yüklenirken hata oluştu', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleAssignToMe = async (ticketId, e) => {
    e.stopPropagation();
    try {
      await ticketsAPI.assignToMe(ticketId);
      showToast('Talep size atandı', 'success');
      loadTickets();
    } catch (error) {
      showToast('Atama yapılırken hata oluştu', 'error');
    }
  };

  const filteredTickets = tickets.filter(ticket => {
    if (!filters.search) return true;
    const searchLower = filters.search.toLowerCase();
    return ticket.title.toLowerCase().includes(searchLower) ||
           ticket.id.toString().includes(searchLower);
  });

  return (
    <div className="dashboard">
      <Navbar />
      
      <div className="dashboard-content">
        <div className="dashboard-header">
          <div>
            <h1>IT Destek Paneli</h1>
            <p>Tüm destek taleplerini görüntüleyin ve yönetin</p>
          </div>
        </div>

        <StatsSection tickets={tickets} />

        <div className="filters">
          <input
            type="text"
            placeholder="🔍 Talep ara (başlık veya #ID)..."
            value={filters.search}
            onChange={(e) => setFilters({...filters, search: e.target.value})}
            style={{ flex: 1, maxWidth: '300px' }}
          />
          <select value={filters.status} onChange={(e) => setFilters({...filters, status: e.target.value})}>
            <option value="">Tüm Durumlar</option>
            <option value="Açık">Açık</option>
            <option value="İşleme Alındı">İşleme Alındı</option>
            <option value="Beklemede">Beklemede</option>
            <option value="Çözüldü">Çözüldü</option>
            <option value="Kapatıldı">Kapatıldı</option>
          </select>
          <select value={filters.category} onChange={(e) => setFilters({...filters, category: e.target.value})}>
            <option value="">Tüm Kategoriler</option>
            <option value="Donanım">Donanım</option>
            <option value="Yazılım">Yazılım</option>
            <option value="Ağ/İnternet">Ağ/İnternet</option>
            <option value="Şifre Sıfırlama">Şifre Sıfırlama</option>
            <option value="Diğer">Diğer</option>
          </select>
          <select value={filters.priority} onChange={(e) => setFilters({...filters, priority: e.target.value})}>
            <option value="">Tüm Öncelikler</option>
            <option value="Acil">Acil</option>
            <option value="Yüksek">Yüksek</option>
            <option value="Orta">Orta</option>
            <option value="Düşük">Düşük</option>
          </select>
        </div>

        {loading ? (
          <div className="loading">Yükleniyor...</div>
        ) : filteredTickets.length === 0 ? (
          <div className="empty-state">
            <p>Filtrelere uygun talep bulunamadı</p>
          </div>
        ) : (
          <div className="tickets-grid">
            {filteredTickets.map(ticket => (
              <div 
                key={ticket.id} 
                className={`ticket-card ${ticket.priority === 'Acil' ? 'urgent' : ''}`}
                onClick={() => navigate(`/ticket/${ticket.id}`)}
              >
                <div className="ticket-card-header">
                  <span className="ticket-id">#{ticket.id}</span>
                  <span className="ticket-status" style={{backgroundColor: getStatusColor(ticket.status)}}>
                    {ticket.status}
                  </span>
                </div>
                <h3 className="ticket-title">{ticket.title}</h3>
                <div className="ticket-meta">
                  <span className="ticket-category">📂 {ticket.category}</span>
                  <span className="ticket-priority" style={{color: getPriorityColor(ticket.priority)}}>
                    ⚡ {ticket.priority}
                  </span>
                </div>
                <div className="ticket-footer">
                  <span className="ticket-date">{formatDate(ticket.created_at)}</span>
                  {!ticket.assigned_to_id && ticket.status === 'Açık' && (
                    <button 
                      className="assign-btn"
                      onClick={(e) => handleAssignToMe(ticket.id, e)}
                    >
                      Üstüme Al
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ITDashboard;
