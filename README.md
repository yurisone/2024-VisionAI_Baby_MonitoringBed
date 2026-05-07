
# 🛏️ Vision AI 기반 스마트 아기침대 시스템 (2024.03 ~ 2024.11)

시각장애인 부모의 안전한 육아를 지원하기 위해 영아의 수면 상태를 실시간으로 모니터링하고 돌연사 위험(뒤집힘, 역류 등) 감지 시 액추에이터를 통해 침대의 위치를 자동으로 제어하는 **Vision AI 기반 하드웨어 통합 제어 시스템입니다.**

Jetson Nano 기반 객체 감지 결과를 활용해 영아 상태를 추정하고 STM32 기반의 펌웨어를 통해 네트워크 서버와 통신하며 침대의 4가지 핵심 안전 동작(뒤집기, 역류 방지, 스윙, 트림 유도)을 물리적으로 제어하도록 구현했습니다.

---

## 🔧 Tech Stack

### Hardware & MCU
- **MCU**: STM32F429ZI (ARM Cortex-M), NVIDIA Jetson Nano, Raspberry Pi 4B
- **Modules**: ESP8266 (ESP-01 Wi-Fi 모듈), L298N 모터 드라이버
- **Actuators**: 리니어 액추에이터, DC 모터, 서보모터
- **Sensors**: 카메라 모듈(IMX219), 비접촉 체온 센서(GY-906), 마이크로웨이브 센서(MR60BHA1), 온습도 센서(DHT22)

### Software & Protocols
- **Languages**: C/C++ (STM32), Python (Jetson Nano)
- **Protocols**: UART (AT Command 기반 통신), HTTP / REST API
- **AI & Vision**: OpenCV, YOLOv5
- **Server**: Flask, Spring Boot, MySQL

---

## 🖥 시스템 아키텍처

카메라 영상 데이터 수집 → Jetson Nano (YOLOv5 추론 및 신뢰도 기반 상태 판단) → HTTP 통신(Flask 서버 전송) → ESP8266 통신(UART) → STM32 제어 명령 수신 → L298N 기반 액추에이터 구동 (역류 방지 및 뒤집기 제어)
<img width="1136" height="502" alt="image" src="https://github.com/user-attachments/assets/c1c8bba7-cf06-4f89-bb77-96e695bcb9ae" />

## 🔌 Hardware Architecture
<img width="1467" height="670" alt="image" src="https://github.com/user-attachments/assets/c6434583-61db-4bf9-9931-d2aa7d67c436" />



---

## 🚀 주요 기능

### 1. Vision AI 기반 수면 상태 모니터링 (뒤집힘 감지)
- Jetson Nano와 카메라를 연동하여 영아의 자세를 실시간으로 인식하고, 영아 돌연사 증후군을 유발할 수 있는 '엎드린 자세(뒤집힘)'를 판별하여 서버로 상태값 전송.

### 2. 하드웨어 액추에이터 기반 안전 제어 동작
- **뒤집기 기능**: 영아 엎드림 감지 시, 시저 리프트와 액추에이터를 제어해 침대 매트리스 각도를 조절하여 영아 자세 복원을 보조.
- **역류 방지 및 스윙**: 식후 역류 방지를 위해 상체 각도를 조절하는 액추에이터 제어 및 숙면을 유도하는 DC 모터 스윙 기능 구현.

### 3. Fail-Safe 로컬 백업 제어 모드
- 네트워크 장애(SPOF) 발생 시에도 아기의 안전을 확보할 수 있도록, 서버 연결 없이 STM32 단독으로 모터를 구동할 수 있는 물리 버튼 기반 로컬 제어 시스템 구축.

---

## 👨‍💻 My Role
- **팀장 역할 총괄**: WBS 기반 프로젝트 일정 관리 및 하드웨어-소프트웨어(서버/앱) 통합 연동 파이프라인 구축
- **Jetson Nano 기반 Vision AI 연동**: YOLOv5 기반 객체 감지 결과를 활용한 영아 상태 판단 로직 구현 및 Flask 서버 연동
- **상태 기반 액추에이터 제어 알고리즘 설계**: 영아 상태값과 사용자 요청 조건에 따라 뒤집기, 역류 방지, 스윙 기능이 동작하는 상태 전이 흐름 및 제어 로직 설계
- **로컬 백업(Fail-Safe) 제어 구조 설계**: 통신 장애 시나리오에 대비하여 MCU(STM32) 로컬 제어 로직을 독립적으로 설계하여 시스템 신뢰성 확보
- 액추에이터 및 센서 구조를 고려한 침대 프레임 설계 및 제작 참여
<img width="1154" height="679" alt="image" src="https://github.com/user-attachments/assets/d1afffe7-c24a-475f-a846-6c3eb6b78c22" />




---

## 🛠 Troubleshooting

### 1. 엣지 환경을 고려한 신뢰도(Confidence) 임계값 기반 자세 판단 로직 설계
**문제**: 영아의 얼굴과 엎드린 자세를 직접 라벨링하여 커스텀 모델을 학습시키기에는 데이터 수집의 한계와 엣지 디바이스(Jetson Nano)의 리소스(연산 속도) 제약이 존재했습니다.
<br><br>
**해결**: 무거운 커스텀 학습 대신 이미 학습된 가벼운 YOLOv5 모델의 `person` 클래스 인식 결과를 역이용하는 알고리즘을 고안했습니다. 영아가 정면을 보고 있을 때는 객체 인식 신뢰도(Confidence Score)가 높게(0.7 이상) 측정되지만, 위험 상황인 **'뒤집힌 자세'가 되면 얼굴과 상체가 가려져 신뢰도가 급격히 하락하는 특성에 착안**했습니다. 이를 통해 신뢰도가 특정 임계값 이하로 떨어지면 '위험(뒤집힘)' 상태로 서버에 전송하는 **필터링 알고리즘을 구현**하여, 연산 리소스를 최적화함과 동시에 시스템의 목적(위험 감지)을 안정적으로 달성했습니다.

### 2. 네트워크 장애 대비 STM32 로컬 백업(Fail-Safe) 제어 구현
**문제**: 클라우드 서버(Spring Boot/Flask)를 거쳐 하드웨어를 제어하는 구조는 통신 지연이나 전시장 등 네트워크 과부하 환경에서 시스템 전체가 마비되는 단일 실패 지점(SPOF) 위험이 있었습니다.
<br><br>
**해결**: 외부 서버와의 통신이 끊어지더라도 핵심 안전 기능(뒤집기, 역류 방지 등)이 무조건 동작해야 한다고 판단했습니다. 이에 따라 STM32 펌웨어 단에서 네트워크 연결 상태를 모니터링하고, 통신 장애가 감지되거나 비상 상황 발생 시 즉각적으로 MCU에 연결된 **물리 버튼 인터럽트를 통해 액추에이터를 직접 구동하는 '로컬 백업 제어 로직'을 설계**했습니다. 실제로 공모전 시연 당일 발생한 네트워크 병목 상황에서 이 백업 로직을 통해 성공적으로 모터를 제어하며 하드웨어 신뢰성을 입증했습니다.

---

## 🎥 Demo Video

https://youtu.be/ajoSamOnoHk

---

## 📈 Result

- **[은상]** 2024년 프로보노 ICT멘토링 공모전 수상
- **[최우수 논문상]** ACK 2024 한국정보처리학회 학술대회 논문상 수상
- 무거운 AI 모델 대신 임계값 필터링 로직을 활용한 **엣지 디바이스 리소스 최적화 경험 확보**
- 네트워크 예외 상황을 고려한 **임베디드 Fail-Safe 시스템 설계 역량 확보**

---

<br>
<br>

**[📂 Additional Demo]**

1. 하드웨어 액추에이터 제어 (트림유도 / 스윙 / 역류방지 / 뒤집기)
**트림유도**
<img width="1040" height="586" alt="image" src="https://github.com/user-attachments/assets/ab4e2d33-1adb-4b0f-b209-8ca9c7a73b1a" />
**스윙**
<img width="1021" height="575" alt="image" src="https://github.com/user-attachments/assets/b4cafbaf-3285-4449-aab4-da322cf87b94" />
**역류방지**
<img width="1028" height="579" alt="image" src="https://github.com/user-attachments/assets/b0996b68-29c5-4093-9344-5218ac9c1a02" />
**뒤집기**
<img width="998" height="563" alt="image" src="https://github.com/user-attachments/assets/38b2a3c0-49aa-4683-9bdb-be0200f9bd5b" />

