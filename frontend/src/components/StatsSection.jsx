/**
 * İstatistik Kartları ve Grafikler
 */

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { PRIORITY_COLORS, STATUS_COLORS } from '../utils/constants';

function StatsSection({ tickets }) {
  // İstatistikleri hesapla
  const openTickets = tickets.filter(t => t.status === 'Açık').length;
  const inProgressTickets = tickets.filter(t => t.status === 'İşleme Alındı').length;
  const resolvedTickets = tickets.filter(t => t.status === 'Çözüldü').length;

  // Kategoriye göre dağılım
  const categoryData = {};
  tickets.forEach(t => {
    categoryData[t.category] = (categoryData[t.category] || 0) + 1;
  });
  const categoryChartData = Object.entries(categoryData).map(([name, value]) => ({
    name,
    value
  }));

  // Önceliğe göre dağılım
  const priorityData = {};
  tickets.forEach(t => {
    priorityData[t.priority] = (priorityData[t.priority] || 0) + 1;
  });
  const priorityChartData = Object.entries(priorityData).map(([name, value]) => ({
    name,
    value
  }));

  const COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Açık Talepler</div>
          <div className="stat-value" style={{color: '#3b82f6'}}>{openTickets}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">İşlemde</div>
          <div className="stat-value" style={{color: '#f59e0b'}}>{inProgressTickets}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Çözüldü</div>
          <div className="stat-value" style={{color: '#10b981'}}>{resolvedTickets}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Toplam Talep</div>
          <div className="stat-value">{tickets.length}</div>
        </div>
      </div>

      {tickets.length > 0 && (
        <div className="charts-section">
          <div className="chart-card">
            <h3>Kategoriye Göre Dağılım</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={categoryChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => entry.name}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {categoryChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>Önceliğe Göre Dağılım</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={priorityChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => entry.name}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {priorityChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </>
  );
}

export default StatsSection;
