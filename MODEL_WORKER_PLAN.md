# GPU Model Worker — अगला चरण

मुख्य लक्ष्य RVC आधारित voice conversion है:
1. authenticated user + voice-owner consent जाँचें।
2. FFmpeg से वीडियो का audio निकालें और original track सुरक्षित रखें।
3. authorized target voice का trained RVC model चुनें।
4. RVC inference चलाएँ; pitch/timing/delivery को यथासंभव source के करीब रखें।
5. converted audio को FFmpeg से वीडियो में mux करें।
6. job status और MP4 download URL लौटाएँ।

RVC conceptual interface:
    convert_voice(input_audio_path, target_model_path, output_audio_path)

RVC implementation/version के अनुसार वास्तविक command अलग होगी। Tested version और model license pin करें।
केवल अपनी या स्पष्ट अनुमति वाली आवाज़ के लिए इस्तेमाल करें। Profile samples निजी रखें, encryption,
authentication, deletion और retention controls लागू करें।

महत्वपूर्ण: RVC voice conversion और cloned-voice TTS अलग तकनीकें हैं।
RVC source performance को अधिक हद तक बनाए रखने के लिए उपयुक्त है; TTS text से नई speech बनाता है।
