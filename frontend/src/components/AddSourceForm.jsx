"""
Add Source Form Component
"""
import React, { useState } from 'react';
import '../styles/AddSourceForm.css';

function AddSourceForm({ onSubmit, onCancel }) {
  const [sourceType, setSourceType] = useState('folder');
  const [formData, setFormData] = useState({
    name: '',
    source_type: 'folder',
    config: {},
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name.startsWith('config.')) {
      const configKey = name.slice(7);
      setFormData({
        ...formData,
        config: { ...formData.config, [configKey]: value },
      });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      name: formData.name,
      source_type: sourceType,
      config: {
        ...formData.config,
        source_type: sourceType,
      },
    });
  };

  return (
    <form className="add-source-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Name</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="My Documents"
          required
        />
      </div>

      <div className="form-group">
        <label>Source Type</label>
        <select
          value={sourceType}
          onChange={(e) => {
            setSourceType(e.target.value);
            setFormData({
              ...formData,
              source_type: e.target.value,
              config: {},
            });
          }}
        >
          <option value="folder">📁 Folder/Files</option>
          <option value="database">🗄️ Database</option>
          <option value="sharepoint">☁️ SharePoint</option>
        </select>
      </div>

      {sourceType === 'folder' && (
        <div className="form-group">
          <label>Folder Path</label>
          <input
            type="text"
            name="config.path"
            value={formData.config.path || ''}
            onChange={handleChange}
            placeholder="C:\Users\Rajiv Singh\Desktop\RAG_PIPELINE\Database"
            required
          />
        </div>
      )}

      {sourceType === 'database' && (
        <>
          <div className="form-group">
            <label>Database Type</label>
            <select
              name="config.type"
              value={formData.config.type || ''}
              onChange={handleChange}
            >
              <option value="">Select...</option>
              <option value="postgresql">PostgreSQL</option>
              <option value="mysql">MySQL</option>
              <option value="mongodb">MongoDB</option>
            </select>
          </div>
          <div className="form-group">
            <label>Connection String</label>
            <input
              type="text"
              name="config.connection_string"
              onChange={handleChange}
              placeholder="postgresql://user:pass@host:5432/db"
            />
          </div>
        </>
      )}

      {sourceType === 'sharepoint' && (
        <>
          <div className="form-group">
            <label>Site URL</label>
            <input
              type="text"
              name="config.site_url"
              onChange={handleChange}
              placeholder="https://tenant.sharepoint.com/sites/sitename"
            />
          </div>
          <div className="form-group">
            <label>Client ID</label>
            <input
              type="text"
              name="config.client_id"
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label>Client Secret</label>
            <input
              type="password"
              name="config.client_secret"
              onChange={handleChange}
            />
          </div>
        </>
      )}

      <div className="form-actions">
        <button type="submit" className="btn-primary">
          Add Source
        </button>
        <button
          type="button"
          className="btn-secondary"
          onClick={onCancel}
        >
          Cancel
        </button>
      </div>
    </form>
  );
}

export default AddSourceForm;
