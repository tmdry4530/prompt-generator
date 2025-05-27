import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from './ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';

// API 기본 URL
const API_BASE_URL = 'http://localhost:5000/api';

// 모델 타입 정의
interface Model {
  model_id: string;
  model_name: string;
  provider: string;
  category: string;
  capabilities: string[];
  supports_multimodal: boolean;
}

interface ModelSelectorProps {
  onModelSelect: (modelId: string) => void;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ onModelSelect }) => {
  // 상태 관리
  const [models, setModels] = useState<Model[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('text');
  const [selectedModelId, setSelectedModelId] = useState<string>('');
  const [modelTips, setModelTips] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // 컴포넌트 마운트 시 모델 목록 가져오기
  useEffect(() => {
    fetchModels();
  }, []);

  // 모델 선택 시 해당 모델의 팁 가져오기
  useEffect(() => {
    if (selectedModelId) {
      fetchModelTips(selectedModelId);
      onModelSelect(selectedModelId);
    }
  }, [selectedModelId, onModelSelect]);

  // 카테고리 변경 시 해당 카테고리의 첫 번째 모델 선택
  useEffect(() => {
    const categoryModels = models.filter(model => model.category === selectedCategory);
    if (categoryModels.length > 0 && (!selectedModelId || !categoryModels.some(model => model.model_id === selectedModelId))) {
      setSelectedModelId(categoryModels[0].model_id);
    }
  }, [selectedCategory, models, selectedModelId]);

  // 모델 목록 가져오기
  const fetchModels = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/models`);
      if (response.data.success) {
        setModels(response.data.models);
        // 첫 번째 카테고리의 첫 번째 모델을 기본 선택
        if (response.data.models.length > 0) {
          const textModels = response.data.models.filter((model: Model) => model.category === 'text');
          if (textModels.length > 0) {
            setSelectedModelId(textModels[0].model_id);
          } else {
            setSelectedModelId(response.data.models[0].model_id);
          }
        }
      } else {
        setError('모델 목록을 가져오는 데 실패했습니다.');
      }
    } catch (error) {
      console.error('모델 목록 가져오기 오류:', error);
      setError('서버 연결에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  // 모델 팁 가져오기
  const fetchModelTips = async (modelId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/model/${modelId}/tips`);
      if (response.data.success) {
        setModelTips(response.data.tips);
      }
    } catch (error) {
      console.error('모델 팁 가져오기 오류:', error);
    }
  };

  // 카테고리별 모델 필터링
  const getModelsByCategory = (category: string) => {
    return models.filter(model => model.category === category);
  };

  // 카테고리별 모델 제공업체 그룹화
  const getGroupedModelsByCategory = (category: string) => {
    const categoryModels = getModelsByCategory(category);
    return categoryModels.reduce((acc, model) => {
      if (!acc[model.provider]) {
        acc[model.provider] = [];
      }
      acc[model.provider].push(model);
      return acc;
    }, {} as Record<string, Model[]>);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>AI 모델 선택</CardTitle>
        <CardDescription>
          프롬프트를 최적화할 AI 모델을 선택하세요
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Tabs 
            defaultValue="text" 
            value={selectedCategory} 
            onValueChange={setSelectedCategory}
            className="w-full"
          >
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="text">텍스트</TabsTrigger>
              <TabsTrigger value="image">이미지</TabsTrigger>
              <TabsTrigger value="video">비디오</TabsTrigger>
              <TabsTrigger value="music">음악</TabsTrigger>
            </TabsList>
            
            <TabsContent value="text" className="mt-4">
              <Select value={selectedModelId} onValueChange={setSelectedModelId}>
                <SelectTrigger>
                  <SelectValue placeholder="텍스트 모델 선택" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(getGroupedModelsByCategory('text')).map(([provider, providerModels]) => (
                    <React.Fragment key={provider}>
                      <div className="px-2 py-1.5 text-sm font-semibold">{provider}</div>
                      {providerModels.map((model) => (
                        <SelectItem key={model.model_id} value={model.model_id}>
                          {model.model_name}
                        </SelectItem>
                      ))}
                    </React.Fragment>
                  ))}
                </SelectContent>
              </Select>
            </TabsContent>
            
            <TabsContent value="image" className="mt-4">
              <Select value={selectedModelId} onValueChange={setSelectedModelId}>
                <SelectTrigger>
                  <SelectValue placeholder="이미지 모델 선택" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(getGroupedModelsByCategory('image')).map(([provider, providerModels]) => (
                    <React.Fragment key={provider}>
                      <div className="px-2 py-1.5 text-sm font-semibold">{provider}</div>
                      {providerModels.map((model) => (
                        <SelectItem key={model.model_id} value={model.model_id}>
                          {model.model_name}
                        </SelectItem>
                      ))}
                    </React.Fragment>
                  ))}
                </SelectContent>
              </Select>
            </TabsContent>
            
            <TabsContent value="video" className="mt-4">
              <Select value={selectedModelId} onValueChange={setSelectedModelId}>
                <SelectTrigger>
                  <SelectValue placeholder="비디오 모델 선택" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(getGroupedModelsByCategory('video')).map(([provider, providerModels]) => (
                    <React.Fragment key={provider}>
                      <div className="px-2 py-1.5 text-sm font-semibold">{provider}</div>
                      {providerModels.map((model) => (
                        <SelectItem key={model.model_id} value={model.model_id}>
                          {model.model_name}
                        </SelectItem>
                      ))}
                    </React.Fragment>
                  ))}
                </SelectContent>
              </Select>
            </TabsContent>
            
            <TabsContent value="music" className="mt-4">
              <Select value={selectedModelId} onValueChange={setSelectedModelId}>
                <SelectTrigger>
                  <SelectValue placeholder="음악 모델 선택" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(getGroupedModelsByCategory('music')).map(([provider, providerModels]) => (
                    <React.Fragment key={provider}>
                      <div className="px-2 py-1.5 text-sm font-semibold">{provider}</div>
                      {providerModels.map((model) => (
                        <SelectItem key={model.model_id} value={model.model_id}>
                          {model.model_name}
                        </SelectItem>
                      ))}
                    </React.Fragment>
                  ))}
                </SelectContent>
              </Select>
            </TabsContent>
          </Tabs>
          
          {loading && <div className="text-center py-4">모델 목록을 불러오는 중...</div>}
          {error && <div className="text-red-500 py-2">{error}</div>}
        </div>
      </CardContent>
      <CardFooter className="flex-col items-start">
        <h4 className="text-sm font-semibold mb-2">모델 최적화 팁:</h4>
        {modelTips.length > 0 ? (
          <ul className="text-sm text-gray-600 list-disc pl-5 space-y-1">
            {modelTips.map((tip, index) => (
              <li key={index}>{tip}</li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-gray-500">이 모델에 대한 팁이 없습니다.</p>
        )}
      </CardFooter>
    </Card>
  );
};

export default ModelSelector;
