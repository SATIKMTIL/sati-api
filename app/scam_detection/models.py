class ScamReport:
    """Scam report model schema"""
    
    @staticmethod
    def validate_analysis_request(data):
        """Validate scam analysis request"""
        errors = []
        
        if not data.get('conversation_text'):
            errors.append('Conversation text is required')
        elif len(data.get('conversation_text', '')) < 10:
            errors.append('Conversation text is too short (minimum 10 characters)')
            
        return errors

    @staticmethod
    def classify_status(confidence_score):
        """Classify status based on confidence score"""
        if confidence_score >= 0.75:
            return 'danger'
        elif confidence_score >= 0.40:
            return 'warning'
        else:
            return 'normal'
