import React, { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { documentService } from '../services/api';
import { Trash2, FileText } from 'lucide-react';

const MyDocumentsPage = () => {
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchDocuments = async () => {
        try {
            const res = await documentService.list();
            setDocuments(res.data || []);
        } catch (error) {
            console.error("Failed to load documents", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDocuments();
    }, []);

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure you want to delete this document?")) return;
        try {
            await documentService.delete(id);
            setDocuments(docs => docs.filter(d => d.id !== id));
        } catch (error) {
            alert("Failed to delete");
        }
    };

    return (
        <div className="documents-page">
            <h1>My Documents</h1>

            {loading ? (
                <p>Loading...</p>
            ) : (
                <div className="documents-list">
                    {documents.length === 0 ? (
                        <Card>No documents found.</Card>
                    ) : (
                        documents.map((doc) => (
                            <Card key={doc.id} className="doc-item">
                                <div className="doc-info">
                                    <FileText size={24} color="#666" />
                                    <div className="doc-meta">
                                        <div className="doc-name">{doc.name}</div>
                                        <div className="doc-date">{doc.date || 'Unknown Date'}</div>
                                    </div>
                                </div>
                                <div className="doc-status status-success">
                                    Processed
                                </div>
                                <Button variant="ghost" onClick={() => handleDelete(doc.id)}>
                                    <Trash2 size={18} color="red" />
                                </Button>
                            </Card>
                        ))
                    )}
                </div>
            )}
        </div>
    );
};

export default MyDocumentsPage;
