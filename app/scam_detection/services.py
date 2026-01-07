import google.generativeai as genai
import logging
import json
import re
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

logger = logging.getLogger(__name__)


class SpeechToTextService:
    """Service for converting speech audio files to text"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        logger.info("SpeechToTextService initialized")
    
    def convert_audio_to_text(self, audio_file, language="th-TH"):
        """
        Convert audio file to text using Google Speech Recognition
        
        Args:
            audio_file: File object (from Flask request.files)
            language: Language code (default: Thai)
        
        Returns:
            str: Transcribed text from the audio
        
        Raises:
            Exception: If transcription fails
        """
        temp_audio_path = None
        temp_wav_path = None
        
        try:
            # Get file extension
            filename = audio_file.filename
            extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'wav'
            
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(suffix=f'.{extension}', delete=False) as temp_audio:
                audio_file.save(temp_audio)
                temp_audio_path = temp_audio.name
            
            # Convert to WAV format if necessary (SpeechRecognition works best with WAV)
            if extension != 'wav':
                temp_wav_path = tempfile.mktemp(suffix='.wav')
                audio = AudioSegment.from_file(temp_audio_path, format=extension)
                audio.export(temp_wav_path, format='wav')
                audio_path_for_recognition = temp_wav_path
            else:
                audio_path_for_recognition = temp_audio_path
            
            # Perform speech recognition
            with sr.AudioFile(audio_path_for_recognition) as source:
                audio_data = self.recognizer.record(source)
                
            # Use Google Web Speech API (free, no API key required)
            text = self.recognizer.recognize_google(audio_data, language=language)
            
            logger.info(f"Successfully transcribed audio: {len(text)} characters")
            return text
            
        except sr.UnknownValueError:
            logger.warning("Speech Recognition could not understand audio")
            raise Exception("ไม่สามารถแปลงเสียงเป็นข้อความได้ กรุณาตรวจสอบว่าไฟล์เสียงชัดเจนและมีเสียงพูด")
        except sr.RequestError as e:
            logger.error(f"Speech Recognition service error: {str(e)}")
            raise Exception(f"เกิดข้อผิดพลาดในการเชื่อมต่อ Speech Recognition service: {str(e)}")
        except Exception as e:
            logger.error(f"Audio conversion error: {str(e)}")
            raise Exception(f"เกิดข้อผิดพลาดในการแปลงไฟล์เสียง: {str(e)}")
        finally:
            # Clean up temporary files
            if temp_audio_path and os.path.exists(temp_audio_path):
                try:
                    os.remove(temp_audio_path)
                except:
                    pass
            if temp_wav_path and os.path.exists(temp_wav_path):
                try:
                    os.remove(temp_wav_path)
                except:
                    pass


class ScamDetectionService:
    def __init__(self, api_key):
        """Initialize Gemini AI service"""
        genai.configure(api_key=api_key)
        # Use stable Gemini Pro model for production reliability
        print(api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("Scam Detection Service initialized with Gemini AI")

    def analyze_conversation(self, conversation_text):
        """
        Analyze conversation text to detect scam patterns
        Returns: dict with status, confidence_score, reason, and red_flags
        """
        try:
            prompt = self._build_analysis_prompt(conversation_text)
            
            response = self.model.generate_content(prompt)
            result = self._parse_analysis_response(response.text)
            
            logger.info(f"Scam analysis completed: {result['status']} (confidence: {result['confidence_score']})")
            return result
            
        except Exception as e:
            logger.error(f"Scam analysis error: {str(e)}")
            raise Exception(f"Failed to analyze conversation: {str(e)}")

    def _build_analysis_prompt(self, conversation_text):
        """Build detailed prompt for scam detection"""
        return f"""คุณเป็นผู้เชี่ยวชาญในการวิเคราะห์และตรวจจับมิจฉาชีพออนไลน์ในประเทศไทย 
วิเคราะห์บทสนทนาต่อไปนี้และประเมินว่ามีความเป็นไปได้แค่ไหนที่บุคคลที่โทรมาเป็นมิจฉาชีพหรือสแกมเมอร์

บทสนทนา:
{conversation_text}

กรุณาวิเคราะห์และตอบกลับในรูปแบบ JSON ที่มีโครงสร้างดังนี้:
{{
  "confidence_score": <ตัวเลขระหว่าง 0.0 - 1.0 ที่แสดงความมั่นใจว่าเป็นสแกม>,
  "status": "<danger|warning|normal>",
  "reason": "<คำอธิบายโดยละเอียดเป็นภาษาไทยว่าทำไมถึงให้คะแนนนี้>",
  "red_flags": [<รายการสัญญาณเตือนภัยที่พบในบทสนทนา>]
}}

เกณฑ์การประเมิน:
- danger: มีความเป็นไปได้สูงมาก (>= 0.75) ที่เป็นมิจฉาชีพ พบสัญญาณเตือนภัยหลายอย่าง
- warning: มีความเป็นไปได้ปานกลาง (0.40 - 0.74) พบสัญญาณน่าสงสัยบางอย่าง
- normal: ความเป็นไปได้ต่ำ (< 0.40) ไม่พบสัญญาณเตือนภัยที่สำคัญ

สัญญาณเตือนภัยที่ควรระวัง:
1. ขอเงินโดยตรงหรือขอโอนเงิน
2. สร้างความเร่งรีบหรือกดดันให้ตัดสินใจทันที
3. อ้างว่าเป็นเจ้าหน้าที่จากหน่วยงานราชการ ธนาคาร หรือบริษัทที่เชื่อถือได้
4. ขอข้อมูลส่วนตัวที่ละเอียดอ่อน เช่น รหัสผ่าน PIN เลขบัตรประชาชน
5. เสนอรางวัลหรือโปรโมชั่นที่ดูดีเกินจริง
6. มีภาษาที่สร้างความกลัว เช่น คุณจะถูกจับ บัญชีจะถูกปิด
7. มีข้อผิดพลาดทางภาษาหรือไวยากรณ์มากผิดปกติ
8. ขอให้ดาวน์โหลดแอปพลิเคชันหรือคลิกลิงก์ที่ไม่รู้จัก
9. อ้างว่าเป็นญาติหรือเพื่อนที่เปลี่ยนเบอร์โทรศัพท์
10. ใช้เทคนิคทางสังคม (Social Engineering) เพื่อหลอกลวง

ตอบกลับเฉพาะ JSON เท่านั้น ไม่ต้องมีข้อความอื่น"""

    def _parse_analysis_response(self, response_text):
        """Parse Gemini's response to extract structured data"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response_text)
            
            # Validate and normalize the response
            confidence_score = float(result.get('confidence_score', 0.5))
            confidence_score = max(0.0, min(1.0, confidence_score))  # Clamp between 0-1
            
            status = result.get('status', '').lower()
            if status not in ['danger', 'warning', 'normal']:
                # Auto-classify based on confidence score
                if confidence_score >= 0.75:
                    status = 'danger'
                elif confidence_score >= 0.40:
                    status = 'warning'
                else:
                    status = 'normal'
            
            return {
                'confidence_score': confidence_score,
                'status': status,
                'reason': result.get('reason', 'ไม่สามารถวิเคราะห์เหตุผลได้'),
                'red_flags': result.get('red_flags', [])
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            # Return default safe result
            return {
                'confidence_score': 0.5,
                'status': 'warning',
                'reason': 'ไม่สามารถวิเคราะห์บทสนทนาได้อย่างสมบูรณ์ กรุณาระมัดระวัง',
                'red_flags': ['ระบบไม่สามารถวิเคราะห์ได้']
            }
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            raise
