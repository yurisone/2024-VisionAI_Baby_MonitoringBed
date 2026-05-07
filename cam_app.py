from camera_stream import Flask, Response
import cv2

app = Flask(__name__)

# 웹캠 초기화 (기본 카메라 사용)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # 카메라에서 프레임을 읽기
        success, frame = camera.read()
        if not success:
            break
        else:

            # 프레임을 JPEG로 인코딩
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # 프레임을 전송
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
