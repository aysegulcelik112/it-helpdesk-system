/**
 * Çalışan Dashboard
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ticketsAPI } from '../services/api';
import { showToast, formatDate, getStatusColor, getPriorityColor } from '../utils/helpers';
import Navbar from '../components/Navbar';
import CreateTicketModal from '../components/CreateTicketModal';
import '../styles/Dashboard.css';

function EmployeeDashboard() {
  const navigate = useNavigate();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState('');

  useEffect(() => {
    loadTickets();
  }, [filterStatus]);

  const loadTickets = async () => {
    try {
      const response = await ticketsAPI.list({ status: filterStatus });
      setTickets(response.data);
    } catch (error) {
      showToast('Talepler yüklenirken hata oluştu', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleTicketCreated = () => {
    setShowCreateModal(false);
    loadTickets();
    showToast('Talep başarıyla oluşturuldu!', 'success');
  };

  const handleCloseTicket = async (ticketId) => {
    if (!confirm('Bu talebi kapatmak istediğinizden emin misiniz?')) return;
    
    try {
      await ticketsAPI.close(ticketId);
      showToast('Talep kapatıldı', 'success');
      loadTickets();
    } catch (error) {
      showToast('Talep kapatılırken hata oluştu', 'error');
    }
  };

  return (
    <div className="dashboard">
      <Navbar />
      
      <div className="dashboard-content">
        <div className="dashboard-header">
          <div>
            <h1>Taleplerim</h1>
            <p>Oluşturduğunuz destek taleplerini görüntüleyin ve yönetin</p>
          </div>
          <button className="create-button" onClick={() => setShowCreateModal(true)}>
            + Yeni Talep Oluştur
          </button>
        </div>

        <div className="filters">
          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="">Tüm Durumlar</option>
            <option value="Açık">Açık</option>
            <option value="İşleme Alındı">İşleme Alındı</option>
            <option value="Beklemede">Beklemede</option>
            <option value="Çözüldü">Çözüldü</option>
            <option value="Kapatıldı">Kapatıldı</option>
          </select>
        </div>

        {loading ? (
          <div className="loading">Yükleniyor...</div>
        ) : tickets.length === 0 ? (
          <div className="empty-state">
            <p>Henüz talep oluşturmadınız</p>
            <button onClick={() => setShowCreateModal(true)}>İlk Talebi Oluştur</button>
          </div>
        ) : (
          <div className="tickets-grid">
            {tickets.map(ticket => (
              <div key={ticket.id} className="ticket-card" onClick={() => navigate(`/ticket/${ticket.id}`)}>
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
                    {ticket.priority}
                  </span>
                </div>
                <div className="ticket-footer">
                  <span className="ticket-date">{formatDate(ticket.created_at)}</span>
                  {ticket.status === 'Çözüldü' && (
                    <button 
                      className="close-ticket-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCloseTicket(ticket.id);
                      }}
                    >
                      Kapat
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showCreateModal && (
        <CreateTicketModal 
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleTicketCreated}
        />
      )}
    </div>
  );
}

export default EmployeeDashboard;
