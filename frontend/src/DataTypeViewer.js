import React, { useState } from 'react';
import { Upload, Table, Alert } from 'lucide-react';

const DataTypeViewer = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/process-data/', {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      
      if (!result.success) {
        throw new Error(result.error);
      }
      
      setData(result.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderColumnInfo = () => {
    if (!data) return null;

    const columns = [
      { field: 'column', header: 'Column Name' },
      { field: 'original_type', header: 'Original Type' },
      { field: 'friendly_type', header: 'Inferred Type' },
      { field: 'null_count', header: 'Missing Values' },
      { field: 'unique_values', header: 'Unique Values' },
    ];

    const rows = Object.entries(data.column_info).map(([column, info]) => ({
      column,
      ...info,
    }));

    return (
      <div className="mt-6">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.field} className="p-2 text-left border bg-gray-100">
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.column}>
                {columns.map((col) => (
                  <td key={col.field} className="p-2 border">
                    {row[col.field]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="w-full max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="p-6 border-b">
        <h2 className="text-2xl font-semibold">Data Type Inference Tool</h2>
      </div>
      <div className="p-6">
        <div className="space-y-4">
          <div className="flex items-center justify-center w-full">
            <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <Upload className="w-8 h-8 mb-2 text-gray-500" />
                <p className="mb-2 text-sm text-gray-500">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-500">CSV or Excel files</p>
              </div>
              <input
                type="file"
                className="hidden"
                accept=".csv,.xlsx,.xls"
                onChange={handleFileUpload}
              />
            </label>
          </div>

          {loading && (
            <div className="text-center">
              <p>Processing file...</p>
            </div>
          )}

          {error && (
            <div className="p-4 text-red-700 bg-red-100 rounded-lg">
              <p> {error.includes('File not provided') ? 'Please upload a file.' : error}</p>
            </div>
          )}

          {data && (
            <div>
              <div className="flex gap-4 mb-4">
                <div className="p-4 bg-gray-100 rounded">
                  <p className="font-semibold">Rows: {data.row_count}</p>
                </div>
                <div className="p-4 bg-gray-100 rounded">
                  <p className="font-semibold">Columns: {data.column_count}</p>
                </div>
              </div>
              {renderColumnInfo()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DataTypeViewer;