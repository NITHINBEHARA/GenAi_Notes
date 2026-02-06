import React, { useState } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { documentService } from '../services/api';

const UploadPage = () => {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files[0]) {
            setFile(e.target.files[0]);
            setMessage(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setMessage(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            await documentService.upload(formData);
            setMessage({ type: 'success', text: 'Document uploaded successfully!' });
            setFile(null);
            // Reset input manually if needed
        } catch (error) {
            console.error(error);
            setMessage({ type: 'error', text: 'Failed to upload document.' });
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="upload-page">
            <h1>Upload Documents</h1>
            <Card className="upload-card">
                <div className="upload-area">
                    <input
                        type="file"
                        id="file-upload"
                        onChange={handleFileChange}
                        accept=".pdf,.docx,.txt"
                        style={{ display: 'none' }}
                    />
                    <label htmlFor="file-upload" className="upload-label">
                        <div className="upload-icon">📄</div>
                        <p>{file ? file.name : "Click or Drag to Upload PDF"}</p>
                    </label>
                </div>

                {message && (
                    <div className={`message ${message.type}`}>
                        {message.text}
                    </div>
                )}

                <div className="actions" style={{ marginTop: '1rem', textAlign: 'right' }}>
                    <Button onClick={handleUpload} disabled={!file || uploading}>
                        {uploading ? 'Uploading...' : 'Upload'}
                    </Button>
                </div>
            </Card>
        </div>
    );
};

export default UploadPage;
