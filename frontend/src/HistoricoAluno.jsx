import React, { useState, useEffect } from 'react';
import NovaAvaliacao from './NovaAvaliacao';

const HistoricoAluno = ({ alunoId }) => {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);

  // Efeito para buscar os dados na API do FastAPI quando o componente montar
  useEffect(() => {
    const buscarHistorico = async () => {
      setLoading(true);
      try {
        // Lembre-se de ajustar a URL base se o seu FastAPI rodar em porta diferente
        const response = await fetch(`http://127.0.0.1:8000/alunos/${alunoId}/historico`);
        
        if (!response.ok) {
          throw new Error('Falha ao buscar histórico. Verifique se o aluno existe.');
        }
        
        const json = await response.json();
        setDados(json);
      } catch (error) {
        setErro(error.message);
      } finally {
        setLoading(false);
      }
    };

    if (alunoId) {
      buscarHistorico();
    }
  }, [alunoId]);

  if (loading) return <div className="p-4 text-gray-600">Carregando histórico...</div>;
  if (erro) return <div className="p-4 text-red-500">Erro: {erro}</div>;
  if (!dados) return null;

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      {/* Cabeçalho do Aluno */}
      <div className="flex justify-between items-center border-b pb-4 mb-6">
        {/* Cabeçalho do Aluno */}
      <div className="flex justify-between items-center border-b pb-4 mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Histórico de: {dados.aluno?.nome}</h2>
          <p className="text-sm text-gray-500">ID do Aluno: {dados.aluno?.id}</p>
        </div>
      </div>
      </div>

      {/* Visão Quantitativa: Tabela de Evolução */}
      <h3 className="text-lg font-semibold text-gray-700 mb-3">Visão Quantitativa (Estágios)</h3>
      <div className="overflow-x-auto mb-8">
        <table className="min-w-full bg-white border border-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="py-2 px-4 border-b text-left text-sm font-medium text-gray-500">Período</th>
              <th className="py-2 px-4 border-b text-left text-sm font-medium text-gray-500">Data</th>
              <th className="py-2 px-4 border-b text-left text-sm font-medium text-gray-500">Nível de Letramento</th>
            </tr>
          </thead>
          <tbody>
            {dados.avaliacoes?.map((av) => (
              <tr key={av.id} className="hover:bg-gray-50">
                <td className="py-2 px-4 border-b text-sm text-gray-700">{av.periodo}</td>
                <td className="py-2 px-4 border-b text-sm text-gray-700">
                  {new Date(av.data_avaliacao).toLocaleDateString('pt-BR')}
                </td>
                <td className="py-2 px-4 border-b text-sm font-bold text-indigo-600">
                  {av.nivel_letramento}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Visão Qualitativa: Relatórios */}
      <h3 className="text-lg font-semibold text-gray-700 mb-3">Visão Qualitativa (Acompanhamento)</h3>
      <div className="space-y-4">
        {dados.avaliacoes?.map((av) => (
          <div key={`qual-${av.id}`} className="p-4 border border-gray-200 rounded-md bg-gray-50">
            <h4 className="font-bold text-gray-800 mb-2">Avaliação {av.periodo}</h4>
            
            <div className="mb-2">
              <span className="font-semibold text-green-700">O que já consegue fazer: </span>
              <span className="text-gray-700">{av.habilidades_adquiridas || 'Não registrado'}</span>
            </div>
            
            <div>
              <span className="font-semibold text-orange-600">O que precisa ser estimulado: </span>
              <span className="text-gray-700">{av.pontos_estimulo || 'Não registrado'}</span>
            </div>
          </div>
        ))}
      </div>
      <NovaAvaliacao alunoId={1} />
    </div>
  );
};

export default HistoricoAluno;