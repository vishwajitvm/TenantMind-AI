'use client';

import React, { useState } from 'react';
import Layout from '../../components/Layout';
import { useStore, DocumentFile } from '../../components/store';
import { Upload, Trash2, Eye, EyeOff, Search, FileText, Calendar, PlusCircle, CheckCircle, Database } from 'lucide-react';

export default function DocumentsPage() {
  const { documents, selectedTenant, uploadDocument, deleteDocument } = useStore();
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [selectedDoc, setSelectedDoc] = useState<DocumentFile | null>(null);

  // Upload fields
  const [newFileName, setNewFileName] = useState('');
  const [newFileCategory, setNewFileCategory] = useState('Leases');
  const [newFileSize, setNewFileSize] = useState('2.5 MB');

  const tenantDocs = documents.filter(d => d.tenantId === selectedTenant?.id);
  
  const filteredDocs = tenantDocs.filter(d => {
    const matchesSearch = d.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = categoryFilter === 'All' || d.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  const handleUpload = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFileName.trim()) return;
    uploadDocument({
      name: newFileName.endsWith('.pdf') || newFileName.endsWith('.xlsx') || newFileName.endsWith('.docx') 
        ? newFileName 
        : `${newFileName}.pdf`,
      size: newFileSize,
      category: newFileCategory,
      tenantId: selectedTenant?.id || 'tenant-alpha',
      uploader: 'admin_user'
    });
    setNewFileName('');
  };

  const categories = ['All', 'Leases', 'Maintenance', 'Compliance', 'Financials'];

  return (
    <Layout>
      <div className="space-y-6">
        <h1 className="text-xl font-bold text-slate-100">Document Corpus Manager</h1>

        {/* Upload Form and Filter Layout */}
        <div className="grid lg:grid-cols-3 gap-6">
          
          {/* Upload Module */}
          <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
              <Upload className="h-4 w-4 text-indigo-400" /> Ingest New Document
            </h3>

            <form onSubmit={handleUpload} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">File Name</label>
                <input
                  type="text"
                  required
                  value={newFileName}
                  onChange={(e) => setNewFileName(e.target.value)}
                  placeholder="Lease_Escalation_Rules"
                  className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2 px-3 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Category</label>
                  <select
                    value={newFileCategory}
                    onChange={(e) => setNewFileCategory(e.target.value)}
                    className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2 px-2.5 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="Leases">Leases</option>
                    <option value="Maintenance">Maintenance</option>
                    <option value="Compliance">Compliance</option>
                    <option value="Financials">Financials</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">File Size</label>
                  <input
                    type="text"
                    required
                    value={newFileSize}
                    onChange={(e) => setNewFileSize(e.target.value)}
                    placeholder="2.5 MB"
                    className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2 px-3 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold py-2.5 rounded-xl transition flex items-center justify-center gap-1.5 shadow-md shadow-indigo-600/10"
              >
                <PlusCircle className="h-4 w-4" /> Start Ingestion Pipeline
              </button>
            </form>
          </div>

          {/* Filtering and Listing */}
          <div className="lg:col-span-2 space-y-4">
            
            {/* Controls */}
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="relative flex-1">
                <Search className="absolute left-3.5 top-2.5 h-4.5 w-4.5 text-slate-500" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search files by name..."
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
                />
              </div>

              <div className="flex gap-1.5 overflow-x-auto">
                {categories.map(cat => (
                  <button
                    key={cat}
                    onClick={() => setCategoryFilter(cat)}
                    className={`py-2 px-3 rounded-xl border text-xs font-semibold whitespace-nowrap transition ${
                      categoryFilter === cat
                        ? 'bg-indigo-600/10 border-indigo-500 text-indigo-300'
                        : 'bg-slate-900/40 border-slate-800/80 text-slate-400 hover:bg-slate-900'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            {/* List */}
            <div className="bg-slate-900/20 border border-slate-800 rounded-2xl overflow-hidden">
              <table className="w-full border-collapse text-left text-xs">
                <thead>
                  <tr className="bg-slate-950/60 border-b border-slate-800 text-slate-400 font-bold uppercase tracking-wider">
                    <th className="p-4">Document Title</th>
                    <th className="p-4">Category</th>
                    <th className="p-4">Size</th>
                    <th className="p-4">Ingestion Stage</th>
                    <th className="p-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {filteredDocs.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="p-8 text-center text-slate-500">
                        No indexed files found matching selected criteria.
                      </td>
                    </tr>
                  ) : (
                    filteredDocs.map((doc) => (
                      <tr key={doc.id} className="hover:bg-slate-900/20 transition">
                        <td className="p-4 font-semibold text-slate-200">
                          <div className="flex items-center gap-2">
                            <FileText className="h-4.5 w-4.5 text-indigo-400" />
                            <span>{doc.name}</span>
                          </div>
                        </td>
                        <td className="p-4 text-slate-350">{doc.category}</td>
                        <td className="p-4 text-slate-400 font-mono">{doc.size}</td>
                        <td className="p-4">
                          <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-bold text-[10px] uppercase border ${
                            doc.status === 'indexed'
                              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                              : doc.status === 'processing'
                                ? 'bg-amber-500/10 border-amber-500/20 text-amber-400 animate-pulse'
                                : 'bg-rose-500/10 border-rose-500/20 text-rose-400'
                          }`}>
                            {doc.status}
                          </span>
                        </td>
                        <td className="p-4 text-right space-x-2">
                          <button
                            onClick={() => setSelectedDoc(doc)}
                            className="text-indigo-400 hover:text-indigo-300 p-1 rounded hover:bg-indigo-500/10 transition"
                            title="Inspect metadata details"
                          >
                            <Eye className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => deleteDocument(doc.id)}
                            className="text-rose-400 hover:text-rose-300 p-1 rounded hover:bg-rose-500/10 transition"
                            title="Purge document"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

          </div>
        </div>

        {/* Slide-over details Overlay */}
        {selectedDoc && (
          <div className="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex justify-end">
            <div className="w-full max-w-md bg-slate-900 border-l border-slate-800 h-screen p-6 shadow-2xl space-y-6 flex flex-col justify-between">
              
              <div className="space-y-6">
                <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                  <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
                    <Database className="h-4 w-4 text-indigo-400" /> Grounding Asset Inspection
                  </h3>
                  <button
                    onClick={() => setSelectedDoc(null)}
                    className="text-slate-400 hover:text-slate-200 text-xs font-semibold hover:underline"
                  >
                    Close Panel
                  </button>
                </div>

                <div className="space-y-4">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-slate-500 block">File Title</span>
                    <span className="text-sm font-semibold text-slate-100">{selectedDoc.name}</span>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="text-[10px] uppercase font-bold text-slate-500 block">Category</span>
                      <span className="text-xs text-slate-200">{selectedDoc.category}</span>
                    </div>
                    <div>
                      <span className="text-[10px] uppercase font-bold text-slate-500 block">Vector Database Tokens</span>
                      <span className="text-xs text-indigo-400 font-mono font-bold">
                        {selectedDoc.tokens ? `${selectedDoc.tokens.toLocaleString()} tokens` : 'Awaiting computation'}
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="text-[10px] uppercase font-bold text-slate-500 block">Uploaded By</span>
                      <span className="text-xs text-slate-250">{selectedDoc.uploader}</span>
                    </div>
                    <div>
                      <span className="text-[10px] uppercase font-bold text-slate-500 block">Upload Date</span>
                      <span className="text-xs text-slate-300 flex items-center gap-1">
                        <Calendar className="h-3.5 w-3.5" /> {selectedDoc.uploadedAt}
                      </span>
                    </div>
                  </div>

                  <div>
                    <span className="text-[10px] uppercase font-bold text-slate-500 block">Ingestion State Details</span>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed bg-slate-950 p-3 rounded-xl border border-slate-800">
                      File was mapped to organization scope <code className="bg-slate-900 px-1 rounded text-indigo-400">{selectedDoc.tenantId}</code>. Text extracts were chunked with overlap of 256 tokens and indexed inside standard hierarchical dense vectors.
                    </p>
                  </div>
                </div>
              </div>

              <button
                onClick={() => setSelectedDoc(null)}
                className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold py-2.5 rounded-xl transition"
              >
                Close Metadata Panel
              </button>

            </div>
          </div>
        )}

      </div>
    </Layout>
  );
}
