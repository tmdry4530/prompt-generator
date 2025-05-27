# Google Imagen 3 모델 프롬프트 엔지니어링 가이드라인

## 개요
Google Imagen 3은 텍스트 프롬프트를 기반으로 고품질 이미지를 생성하는 최신 AI 모델입니다. 자연어 설명을 통해 사실적이고 세부적인 이미지를 생성할 수 있으며, 짧은 프롬프트부터 상세한 프롬프트까지 다양한 입력을 지원합니다.

## 프롬프트 작성 기본 원칙

### 1. 주제, 컨텍스트, 스타일 구조화
효과적인 프롬프트는 다음 세 가지 핵심 요소를 포함해야 합니다:
- **주제(Subject)**: 이미지의 중심이 되는 사물, 사람, 동물, 풍경 등
- **컨텍스트/배경(Context)**: 주제가 배치될 환경이나 배경
- **스타일(Style)**: 원하는 이미지의 예술적 스타일이나 표현 방식

예시: "초고층 빌딩(컨텍스트)으로 둘러싸인 현대식 아파트 건물(주제)의 스케치(스타일)"

### 2. 프롬프트 길이와 세부 사항
- **짧은 프롬프트**: 빠른 이미지 생성에 적합하지만 세부 사항이 제한적
- **긴 프롬프트**: 더 많은 세부 사항과 컨트롤을 제공하며 구체적인 이미지 생성 가능
- 반복적인 프롬프트 개선을 통해 원하는 결과에 가까워질 수 있음

### 3. 설명적 언어 사용
- 자세한 형용사와 부사를 사용하여 명확한 이미지 묘사
- 맥락 정보 제공으로 AI의 이해도 향상
- 특정 아티스트나 예술 스타일 참조 가능

## 고급 프롬프트 작성 기법

### 1. 이미지에 텍스트 생성
- 텍스트는 25자(영문 기준) 이하로 제한하여 최적의 결과 도출
- 여러 문구를 사용할 경우 3개 이하로 유지
- 글꼴 스타일, 크기, 배치에 대한 지시 포함 가능
- 반복 생성을 통해 원하는 텍스트 표현 개선

예시: "'Summerland'라는 텍스트가 굵은 서체로 제목으로 표시된 포스터이며 이 텍스트 아래에 'Summer never felt so good'이라는 슬로건이 있습니다."

### 2. 프롬프트 파라미터화
- API 또는 SDK 사용 시 입력을 파라미터화하여 출력 결과 제어 강화
- 템플릿 형식으로 프롬프트 구성하여 일관된 결과 생성

예시: "A {logo_style} logo for a {company_area} company on a solid color background. Include the text {company_name}."

### 3. 스타일 지정
- **사진 스타일**: 사실적인 이미지 생성을 위한 사진 스타일 지정
- **삽화 및 아트 스타일**: 다양한 예술 스타일(수채화, 유화, 디지털 아트 등) 지정
- **역사적 아트 참조**: 특정 시대나 예술 운동의 스타일 참조

### 4. 이미지 품질 수정자
- 해상도, 디테일 수준, 조명 조건 등 품질 관련 수정자 추가
- 카메라 설정(초점 거리, 조리개, 셔터 속도 등) 지정 가능

### 5. 부정적 프롬프트
- 원하지 않는 요소를 명시하여 제외
- 특정 스타일, 객체, 품질 문제 등을 배제하는 지시 포함

## 실전 프롬프트 예시

### 1. 영화적 장면 묘사
```
An epic scene from a high-quality blockbuster movie, depicting the fierce Battle of Beleriand. The elven leader, in shining armor, stands at the forefront of the battlefield, surrounded by chaos as Orcs and other servants of darkness clash with the elven forces. Dynamic camera angles capture the elven forces as they fight with determination, emphasizing their agility and unity amidst the darkness. Hyper-detailed VFX bring the battle to life with sparks flying from each clash of weapons, dust swirling around charging warriors, and arrows whistling through the air.
```

### 2. 캐릭터 디자인
```
A high-resolution, macro-style photograph of a strange, vaguely humanoid creature, approximately 3 meters tall, shot from a 45-degree angle, with a shallow depth of field, focusing on the creature's extremely elongated skull and razor-sharp claws. The creature stands upright on two legs, curved backward in an unnatural posture, with a skeletal thoracic cage visible beneath its white porcelain carapace.
```

### 3. 환경 및 풍경
```
A breathtaking, hand-drawn frame from a Studio Ghibli masterpiece, showcasing an enchanting open-air garden bursting with life. The scene is a symphony of vibrant colors, with each blade of grass and leaf meticulously detailed. Sunlight filters through the canopy of ancient trees, casting dappled shadows across the moss-covered stone pathways that wind through the garden.
```

## 프롬프트 구조화 팁

### 1. 명확성과 구체성
- 장면, 조명, 스타일을 정밀하게 묘사
- 모호한 표현보다 구체적인 설명 사용

### 2. 이미지 묘사
- 생생하고 설명적인 언어로 명확한 시각적 이미지 표현
- 색상, 질감, 형태 등 시각적 요소 상세 기술

### 3. 스타일과 분위기
- 예술적 스타일, 색상 팔레트, 분위기를 명시하여 이미지 톤 설정
- 참조할 아티스트나 작품 스타일 언급 가능

### 4. 행동과 관점
- 장면에서 일어나는 행동 묘사
- 시점이나 카메라 각도 지정

## 제한사항 및 주의사항
- 생성된 이미지는 유해하거나 불쾌감을 주는 콘텐츠를 제외하도록 필터링됨
- 입력 텍스트 프롬프트와 업로드된 이미지도 콘텐츠 필터링 대상
- 책임감 있는 AI 사용 가이드라인 준수 필요
- 의심되는 악용사례나 부적절한 자료는 신고 가능

## 참고 자료
- Google Cloud Vertex AI 공식 문서
- Imagen 3 프롬프트 작성 가이드
- GitHub의 Imagen3 프롬프트 가이드
