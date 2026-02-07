package com.example.smspam.network;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class PredictResponse {
    @SerializedName("status")
    public String status;
    @SerializedName("message")
    public String message;
    @SerializedName("data")
    public PredictData data;

    public static class PredictData {
        @SerializedName("prediction")
        public String prediction;
        @SerializedName("confidence")
        public double confidence;
        @SerializedName("confidence_percent")
        public String confidencePercent;
        @SerializedName("risk_level")
        public String riskLevel;
        @SerializedName("detected_keywords")
        public List<String> detectedKeywords;
        @SerializedName("explanation")
        public List<String> explanation;
    }
}
