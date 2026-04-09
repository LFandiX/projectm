import React, { useState } from 'react';
import { CheckCircle, XCircle, RefreshCw, ChevronRight, Award, Shield, Calculator, AlertTriangle, BarChart } from 'lucide-react';

const RiskQuiz = () => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showScore, setShowScore] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [isAnswered, setIsAnswered] = useState(false);

  const questions = [
    // --- KONSEP DASAR (1-5) ---
    {
      question: "Apa definisi dari 'Risk' (Risiko) dalam konteks keamanan informasi?",
      options: [
        "Keadaan di mana sistem benar-benar aman dari segala ancaman.",
        "Probabilitas ancaman mengeksploitasi kerentanan dan menyebabkan dampak merugikan.",
        "Proses menghapus semua virus dari komputer.",
        "Sebuah perangkat lunak antivirus yang diinstal di server."
      ],
      answer: 1,
      explanation: "Risiko adalah fungsi dari kemungkinan (likelihood) ancaman mengeksploitasi kerentanan (vulnerability) yang menghasilkan dampak (impact) negatif."
    },
    {
      question: "Apa yang dimaksud dengan 'Vulnerability' (Kerentanan)?",
      options: [
        "Aktor jahat yang mencoba merusak sistem.",
        "Kelemahan atau celah dalam aset yang dapat dieksploitasi oleh ancaman.",
        "Kerugian finansial yang dialami perusahaan.",
        "Biaya untuk memperbaiki sistem."
      ],
      answer: 1,
      explanation: "Vulnerability adalah kelemahan (weakness) dalam sistem, prosedur, atau kontrol yang dapat dimanfaatkan oleh ancaman."
    },
    {
      question: "Komponen risiko sering digambarkan dengan rumus logika: Risk = ...?",
      options: [
        "Asset + Threat",
        "Threat x Vulnerability x Impact",
        "Cost - Benefit",
        "Vulnerability / Control"
      ],
      answer: 1,
      explanation: "Model umum risiko (seperti NIST/ISO) sering menggambarkan Risiko sebagai kombinasi dari Ancaman, Kerentanan, dan Dampak (Likelihood x Impact)."
    },
    {
      question: "Apa istilah untuk potensi kejadian yang tidak diinginkan yang dapat membahayakan aset organisasi?",
      options: [
        "Asset (Aset)",
        "Control (Kontrol)",
        "Threat (Ancaman)",
        "Residual Risk (Risiko Sisa)"
      ],
      answer: 2,
      explanation: "Threat (Ancaman) adalah objek, orang, atau entitas lain yang mewakili bahaya bagi aset."
    },
    {
      question: "Manakah yang BUKAN merupakan kategori aset dalam manajemen risiko?",
      options: [
        "Hardware & Software",
        "Data & Informasi",
        "Manusia (People)",
        "Kompetitor Bisnis"
      ],
      answer: 3,
      explanation: "Kompetitor adalah ancaman eksternal, bukan aset internal yang perlu dilindungi dalam inventaris aset risiko."
    },
    // --- PERHITUNGAN RISIKO (6-10) ---
    {
      question: "Apa kepanjangan dari SLE dalam perhitungan risiko kuantitatif?",
      options: [
        "System Loss Estimation",
        "Single Loss Expectancy",
        "Secure Level Encryption",
        "Standard Liability Exposure"
      ],
      answer: 1,
      explanation: "SLE adalah Single Loss Expectancy, yaitu perkiraan kerugian tunggal dari satu kejadian risiko."
    },
    {
      question: "Rumus untuk menghitung SLE adalah:",
      options: [
        "Asset Value x Exposure Factor (EF)",
        "ALE x ARO",
        "Cost - Benefit",
        "Likelihood x Impact"
      ],
      answer: 0,
      explanation: "SLE dihitung dengan mengalikan Nilai Aset (Asset Value) dengan Faktor Paparan (Exposure Factor)."
    },
    {
      question: "Sebuah server bernilai Rp 100.000.000. Jika terjadi kebakaran, diperkirakan 50% server akan rusak (EF=0.5). Berapa SLE-nya?",
      options: [
        "Rp 100.000.000",
        "Rp 50.000.000",
        "Rp 25.000.000",
        "Rp 10.000.000"
      ],
      answer: 1,
      explanation: "SLE = Asset Value (100 Juta) x EF (0.5) = Rp 50.000.000."
    },
    {
      question: "Jika SLE adalah Rp 10.000.000 dan risiko tersebut diperkirakan terjadi 2 kali setahun (ARO=2), berapa ALE (Annualized Loss Expectancy)-nya?",
      options: [
        "Rp 5.000.000",
        "Rp 10.000.000",
        "Rp 12.000.000",
        "Rp 20.000.000"
      ],
      answer: 3,
      explanation: "ALE = SLE x ARO. Rp 10.000.000 x 2 = Rp 20.000.000."
    },
    {
      question: "Dalam perhitungan Cost-Benefit Analysis (CBA), kontrol dianggap layak jika:",
      options: [
        "Biaya kontrol lebih besar dari nilai aset.",
        "Nilai CBA negatif.",
        "Biaya kontrol lebih kecil dari pengurangan risiko (ALE sebelum - ALE sesudah).",
        "Kontrol tersebut paling mahal di pasar."
      ],
      answer: 2,
      explanation: "CBA positif (layak) terjadi jika penghematan dari pengurangan risiko lebih besar daripada biaya implementasi kontrol tersebut."
    },
    // --- RISK TREATMENT (11-15) ---
    {
      question: "Strategi penanganan risiko di mana organisasi menerapkan kontrol keamanan untuk mengurangi dampak atau kemungkinan terjadinya risiko disebut:",
      options: [
        "Risk Acceptance (Menerima)",
        "Risk Transference (Transfer)",
        "Risk Mitigation (Mitigasi)",
        "Risk Termination (Menghentikan)"
      ],
      answer: 2,
      explanation: "Mitigasi adalah usaha mengurangi risiko dengan menerapkan kontrol (misal: firewall, antivirus)."
    },
    {
      question: "Membeli asuransi siber atau menggunakan pihak ketiga (outsourcing) adalah contoh dari strategi:",
      options: [
        "Risk Mitigation",
        "Risk Transference",
        "Risk Acceptance",
        "Risk Avoidance"
      ],
      answer: 1,
      explanation: "Transfer risiko memindahkan beban kerugian finansial atau tanggung jawab pengelolaan kepada pihak lain (seperti asuransi)."
    },
    {
      question: "Jika biaya perlindungan jauh lebih mahal daripada nilai aset itu sendiri, strategi yang paling logis adalah:",
      options: [
        "Risk Acceptance (Terima Risiko)",
        "Risk Mitigation (Pasang Kontrol Mahal)",
        "Risk Termination (Hentikan Bisnis)",
        "Risk Analysis (Analisis Ulang)"
      ],
      answer: 0,
      explanation: "Jika biaya kontrol > dampak kerugian, manajemen biasanya memilih untuk menerima risiko tersebut (Acceptance)."
    },
    {
      question: "Memutuskan untuk tidak meluncurkan fitur produk tertentu karena risikonya terlalu tinggi dan sulit dimitigasi adalah contoh:",
      options: [
        "Risk Mitigation",
        "Risk Transference",
        "Risk Termination/Avoidance",
        "Risk Acceptance"
      ],
      answer: 2,
      explanation: "Termination atau Avoidance adalah menghilangkan risiko dengan cara menghentikan aktivitas yang menyebabkan risiko tersebut."
    },
    {
      question: "Apa yang dimaksud dengan 'Residual Risk' (Risiko Sisa)?",
      options: [
        "Risiko yang ada sebelum kontrol diterapkan.",
        "Risiko yang tersisa setelah kontrol keamanan diterapkan.",
        "Total seluruh risiko dalam organisasi.",
        "Risiko yang ditransfer ke asuransi."
      ],
      answer: 1,
      explanation: "Residual Risk adalah risiko yang masih tertinggal setelah manajemen melakukan upaya mitigasi/kontrol."
    },
    // --- RISK APPETITE & LAINNYA (16-20) ---
    {
      question: "Apa itu 'Risk Appetite'?",
      options: [
        "Keinginan hacker untuk menyerang.",
        "Jumlah dan jenis risiko yang bersedia diterima organisasi untuk mencapai tujuannya.",
        "Daftar menu risiko dalam laporan tahunan.",
        "Total kerugian yang dialami tahun lalu."
      ],
      answer: 1,
      explanation: "Risk Appetite adalah selera risiko, yaitu seberapa besar risiko yang berani diambil atau ditoleransi oleh organisasi."
    },
    {
      question: "Tujuan utama Keamanan Informasi dalam konteks manajemen risiko adalah:",
      options: [
        "Menghilangkan risiko hingga 0%.",
        "Menyelaraskan Residual Risk dengan Risk Appetite.",
        "Membeli semua alat keamanan tercanggih.",
        "Menutup akses internet sepenuhnya."
      ],
      answer: 1,
      explanation: "Risiko tidak bisa 0%. Tujuannya adalah membawa risiko sisa (Residual) ke level yang dapat diterima (sesuai Risk Appetite)."
    },
    {
      question: "Perbedaan utama antara Analisis Risiko Kualitatif dan Kuantitatif adalah:",
      options: [
        "Kualitatif menggunakan angka uang, Kuantitatif menggunakan skala (Low/Med/High).",
        "Kualitatif menggunakan skala (Low/Med/High), Kuantitatif menggunakan nilai numerik/uang.",
        "Kualitatif lebih akurat daripada Kuantitatif.",
        "Tidak ada perbedaan."
      ],
      answer: 1,
      explanation: "Kualitatif bersifat subjektif (skala deskriptif), sedangkan Kuantitatif bersifat objektif (angka finansial/persentase)."
    },
    {
      question: "Manakah di bawah ini yang merupakan langkah PERTAMA dalam proses manajemen risiko?",
      options: [
        "Risk Evaluation",
        "Risk Identification",
        "Risk Treatment",
        "Risk Reporting"
      ],
      answer: 1,
      explanation: "Proses dimulai dengan Risk Identification (Identifikasi aset dan ancaman), baru kemudian dianalisis dan dievaluasi."
    },
    {
      question: "Dokumen yang memetakan hubungan antara Ancaman (Threat), Kerentanan (Vulnerability), dan Aset disebut:",
      options: [
        "Financial Statement",
        "TVA Worksheet (Threat-Vulnerability-Asset)",
        "SLA Document",
        "Network Diagram"
      ],
      answer: 1,
      explanation: "TVA Worksheet digunakan untuk mengidentifikasi pasangan ancaman-kerentanan-aset untuk analisis lebih lanjut."
    }
  ];

  const handleOptionClick = (index) => {
    if (isAnswered) return;
    setSelectedOption(index);
    setIsAnswered(true);
    
    if (index === questions[currentQuestion].answer) {
      setScore(score + 1);
    }
  };

  const handleNextQuestion = () => {
    const nextQuestion = currentQuestion + 1;
    if (nextQuestion < questions.length) {
      setCurrentQuestion(nextQuestion);
      setSelectedOption(null);
      setIsAnswered(false);
    } else {
      setShowScore(true);
    }
  };

  const resetQuiz = () => {
    setCurrentQuestion(0);
    setScore(0);
    setShowScore(false);
    setSelectedOption(null);
    setIsAnswered(false);
  };

  const getScoreMessage = () => {
    const percentage = (score / questions.length) * 100;
    if (percentage >= 80) return "Luar Biasa! Anda menguasai Manajemen Risiko.";
    if (percentage >= 60) return "Bagus! Pemahaman konsep Anda cukup kuat.";
    return "Terus Belajar! Coba pelajari kembali materi PPT.";
  };

  const getCategoryBadge = () => {
    if (currentQuestion < 5) return { color: "bg-purple-100 text-purple-700", label: "Konsep Dasar", icon: <Shield size={14}/> };
    if (currentQuestion < 10) return { color: "bg-green-100 text-green-700", label: "Perhitungan", icon: <Calculator size={14}/> };
    if (currentQuestion < 15) return { color: "bg-orange-100 text-orange-700", label: "Penanganan Risiko", icon: <AlertTriangle size={14}/> };
    return { color: "bg-blue-100 text-blue-700", label: "Analisis & Strategi", icon: <BarChart size={14}/> };
  };

  const badge = getCategoryBadge();

  return (
    // PERBAIKAN DI SINI:
    // w-full = memastikan lebar penuh
    // min-h-screen = memastikan tinggi penuh layar
    // flex items-center justify-center = memastikan konten di tengah
    <div className="min-h-screen w-full bg-slate-100 flex items-center justify-center p-4 font-sans text-slate-800">
      
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-200">
        
        {/* Header */}
        <div className="bg-blue-600 p-6 text-white flex justify-between items-center shadow-md relative z-10">
          <div>
            <h1 className="text-xl md:text-2xl font-bold flex items-center gap-2">
              <Shield className="w-6 h-6" /> Kuis Manajemen Risiko
            </h1>
            <p className="text-blue-100 text-sm mt-1">Berdasarkan Materi PPT & Konsep Dasar</p>
          </div>
          {!showScore && (
            <div className="bg-blue-700/50 backdrop-blur-sm px-4 py-2 rounded-lg font-mono font-bold text-sm md:text-base border border-blue-500">
              {currentQuestion + 1} <span className="text-blue-200 text-xs">/ {questions.length}</span>
            </div>
          )}
        </div>

        {/* Content Area */}
        <div className="p-6 md:p-8">
          {showScore ? (
            <div className="text-center py-8 animate-fade-in">
              <Award className="w-24 h-24 text-yellow-500 mx-auto mb-6 drop-shadow-lg" />
              <h2 className="text-3xl font-bold mb-3 text-slate-800">Kuis Selesai!</h2>
              <p className="text-slate-600 mb-8 text-lg">{getScoreMessage()}</p>
              
              <div className="bg-slate-50 border border-slate-200 p-8 rounded-2xl mb-8 inline-block min-w-[240px] shadow-inner">
                <span className="block text-sm text-slate-500 uppercase tracking-wider font-semibold mb-2">Skor Akhir</span>
                <div className="flex items-baseline justify-center gap-2">
                  <span className="text-6xl font-extrabold text-blue-600">{score}</span>
                  <span className="text-slate-400 text-2xl font-medium">/ {questions.length}</span>
                </div>
              </div>

              <div>
                <button 
                  onClick={resetQuiz}
                  className="flex items-center gap-2 mx-auto bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-all hover:shadow-lg hover:scale-105 active:scale-95"
                >
                  <RefreshCw className="w-5 h-5" /> Coba Lagi
                </button>
              </div>
            </div>
          ) : (
            <>
              {/* Question Section */}
              <div className="mb-8">
                <div className="flex items-center gap-2 mb-4">
                  <span className={`${badge.color} text-xs px-3 py-1 rounded-full font-bold uppercase tracking-wide flex items-center gap-1.5`}>
                    {badge.icon} {badge.label}
                  </span>
                </div>
                
                <h2 className="text-xl md:text-2xl font-semibold leading-relaxed text-slate-800">
                  {questions[currentQuestion].question}
                </h2>
              </div>

              {/* Options */}
              <div className="space-y-3">
                {questions[currentQuestion].options.map((option, index) => {
                  let baseClass = "w-full text-left p-4 rounded-xl border-2 transition-all flex justify-between items-center shadow-sm relative overflow-hidden group ";
                  
                  if (isAnswered) {
                    if (index === questions[currentQuestion].answer) {
                      baseClass += "border-green-500 bg-green-50 text-green-800 font-medium ring-1 ring-green-500";
                    } else if (index === selectedOption) {
                      baseClass += "border-red-500 bg-red-50 text-red-800 font-medium";
                    } else {
                      baseClass += "border-slate-100 bg-slate-50 text-slate-400 opacity-60";
                    }
                  } else {
                    baseClass += "bg-white border-slate-200 hover:border-blue-500 hover:shadow-md hover:translate-x-1 text-slate-700";
                  }

                  return (
                    <button
                      key={index}
                      onClick={() => handleOptionClick(index)}
                      disabled={isAnswered}
                      className={baseClass}
                    >
                      <span className="z-10 relative">{option}</span>
                      {isAnswered && index === questions[currentQuestion].answer && (
                        <CheckCircle className="text-green-600 w-6 h-6 flex-shrink-0 animate-bounce" />
                      )}
                      {isAnswered && index === selectedOption && index !== questions[currentQuestion].answer && (
                        <XCircle className="text-red-500 w-6 h-6 flex-shrink-0 animate-pulse" />
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Explanation & Next Button */}
              {isAnswered && (
                <div className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                  <div className="bg-blue-50 border-l-4 border-blue-500 p-5 rounded-r-xl mb-6 text-slate-700 shadow-sm">
                    <span className="font-bold flex items-center gap-2 mb-2 text-blue-800">
                      <div className="bg-blue-200 p-1 rounded">💡</div> Penjelasan:
                    </span>
                    <p className="leading-relaxed">{questions[currentQuestion].explanation}</p>
                  </div>
                  
                  <button 
                    onClick={handleNextQuestion}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-xl font-bold text-lg flex items-center justify-center gap-2 transition-all hover:shadow-lg hover:bg-blue-700 active:scale-[0.98]"
                  >
                    {currentQuestion === questions.length - 1 ? "Lihat Hasil Akhir" : "Soal Selanjutnya"} <ChevronRight className="w-6 h-6" />
                  </button>
                </div>
              )}
            </>
          )}
        </div>
        
        {/* Progress Bar */}
        {!showScore && (
          <div className="h-2 bg-slate-100 w-full">
            <div 
              className="h-full bg-blue-600 transition-all duration-500 ease-out"
              style={{ width: `${((currentQuestion + (isAnswered ? 1 : 0)) / questions.length) * 100}%` }}
            ></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RiskQuiz;