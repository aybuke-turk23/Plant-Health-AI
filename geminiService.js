const { GoogleGenerativeAI } = require("@google/generative-ai");

// API anahtarını buraya yapıştır veya .env dosyasından çek
const genAI = new GoogleGenerativeAI("BURAYA_API_ANAHTARINI_YAZ");

// Hız ve verimlilik için Flash modelini seçiyoruz
const model = genAI.getGenerativeModel({ 
    model: "gemini-1.5-flash",
    // Yapay zekanın "karakterini" burada belirliyoruz
    systemInstruction: "Sen Plant-Health-AI projesinin uzman ziraat asistanısın. Sadece bitki hastalıkları, bakımı ve tedavisi hakkında teknik ve yardımsever bilgi verirsin. Diğer konularda cevap vermeyi nazikçe reddet."
});

async function generatePlantResponse(diseaseData) {
    try {
        const prompt = `Analiz sonucu: ${diseaseData.plantName} bitkisinde ${diseaseData.disease} tespit edildi. 
                        Güven skoru: %${diseaseData.confidence}. 
                        Lütfen bu durum için tedavi yöntemleri öner.`;

        const result = await model.generateContent(prompt);
        const response = await result.response;
        return response.text();
    } catch (error) {
        console.error("Gemini Hatası:", error);
        return "Öneriler şu an oluşturulamadı, lütfen daha sonra tekrar deneyiniz.";
    }
}

module.exports = { generatePlantResponse };