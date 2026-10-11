import { useQuery } from '@tanstack/react-query';
import { getHealth, getEvaluation, getModelInfo, getComparison } from '@/services/modelService';
import { getHistory } from '@/services/historyService';
export const useHealth = () => useQuery({ queryKey: ['health'], queryFn: getHealth, retry: false, refetchInterval: 30000, staleTime: 15000 });
export const useHistory = () => useQuery({ queryKey: ['history'], queryFn: getHistory, retry: false, staleTime: 30000 });
export const useEvaluation = () => useQuery({ queryKey: ['evaluation'], queryFn: getEvaluation, retry: false });
export const useModelInfo = () => useQuery({ queryKey: ['model-info'], queryFn: getModelInfo, retry: false });
export const useComparison = () => useQuery({ queryKey: ['comparison'], queryFn: getComparison, retry: false });
