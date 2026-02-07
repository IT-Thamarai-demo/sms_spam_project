package com.example.smspam;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.smspam.database.DatabaseHelper;
import com.example.smspam.network.ApiService;
import com.example.smspam.network.PredictRequest;
import com.example.smspam.network.PredictResponse;
import com.example.smspam.network.RetrofitClient;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import com.google.android.material.chip.Chip;
import com.google.android.material.chip.ChipGroup;

public class MainActivity extends AppCompatActivity {

    private EditText etMessage;
    private Button btnScan, btnPaste, btnViewHistory;
    private View cardResult;
    private TextView tvPrediction, tvRisk, tvConfidence;
    private ChipGroup cgKeywords;
    private DatabaseHelper dbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        etMessage = findViewById(R.id.etMessage);
        btnScan = findViewById(R.id.btnScan);
        btnPaste = findViewById(R.id.btnPaste);
        btnViewHistory = findViewById(R.id.btnViewHistory);
        cardResult = findViewById(R.id.cardResult);
        tvPrediction = findViewById(R.id.tvPrediction);
        tvRisk = findViewById(R.id.tvRisk);
        tvConfidence = findViewById(R.id.tvConfidence);
        cgKeywords = findViewById(R.id.cgKeywords);

        dbHelper = new DatabaseHelper(this);

        btnScan.setOnClickListener(v -> performScan());
        btnPaste.setOnClickListener(v -> pasteFromClipboard());
        btnViewHistory.setOnClickListener(v -> startActivity(new Intent(this, HistoryActivity.class)));
    }

    private void pasteFromClipboard() {
        ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
        if (clipboard != null && clipboard.hasPrimaryClip()) {
            etMessage.setText(clipboard.getPrimaryClip().getItemAt(0).getText());
        }
    }

    private void performScan() {
        String msg = etMessage.getText().toString().trim();
        if (msg.isEmpty()) {
            android.util.Log.w("SMS_SPAM", "Scan aborted: empty message");
            Toast.makeText(this, "Please enter a message to scan", Toast.LENGTH_LONG).show();
            return;
        }

        android.util.Log.d("SMS_SPAM",
                "Starting scan for message: " + msg.substring(0, Math.min(50, msg.length())) + "...");
        btnScan.setEnabled(false);
        btnScan.setText("Scanning...");

        ApiService service = RetrofitClient.getService();
        android.util.Log.d("SMS_SPAM", "Making API call to: http://10.173.3.93:5000/predict");

        service.predict(new PredictRequest(msg)).enqueue(new Callback<PredictResponse>() {
            @Override
            public void onResponse(Call<PredictResponse> call, Response<PredictResponse> response) {
                btnScan.setEnabled(true);
                btnScan.setText(getString(R.string.btn_scan));

                android.util.Log.d("SMS_SPAM", "API Response received - Code: " + response.code());

                if (response.isSuccessful() && response.body() != null) {
                    android.util.Log.d("SMS_SPAM", "Response status: " + response.body().status);

                    if ("success".equals(response.body().status)) {
                        PredictResponse.PredictData data = response.body().data;
                        android.util.Log.d("SMS_SPAM",
                                "Prediction: " + data.prediction + ", Confidence: " + data.confidencePercent);
                        displayResult(data);
                        dbHelper.insertHistory(msg, data.prediction, data.confidencePercent, data.riskLevel);
                    } else {
                        String errorMsg = response.body().message != null ? response.body().message
                                : "Unknown error from server";
                        android.util.Log.e("SMS_SPAM", "Server returned error status: " + errorMsg);
                        Toast.makeText(MainActivity.this, "Server Error: " + errorMsg, Toast.LENGTH_LONG).show();
                    }
                } else {
                    String errorMsg = "Server Error (Code " + response.code() + ")";
                    if (response.body() != null && response.body().message != null) {
                        errorMsg += ": " + response.body().message;
                    }
                    android.util.Log.e("SMS_SPAM", errorMsg);
                    Toast.makeText(MainActivity.this, errorMsg, Toast.LENGTH_LONG).show();
                }
            }

            @Override
            public void onFailure(Call<PredictResponse> call, Throwable t) {
                btnScan.setEnabled(true);
                btnScan.setText(getString(R.string.btn_scan));

                android.util.Log.e("SMS_SPAM",
                        "Connection failed: " + t.getClass().getSimpleName() + " - " + t.getMessage());
                t.printStackTrace();

                String userMessage = "Connection Failed!\n\n";
                userMessage += "Error: " + t.getMessage() + "\n\n";
                userMessage += "Troubleshooting:\n";
                userMessage += "1. Make sure backend server is running on port 5000\n";
                userMessage += "2. Make sure phone and PC are on SAME Wi-Fi network\n";
                userMessage += "3. Check firewall settings\n\n";
                userMessage += "Current URL: http://10.173.3.93:5000/";

                Toast.makeText(MainActivity.this, "Connection failed - Check logcat for details", Toast.LENGTH_LONG)
                        .show();

                // Also show in a dialog for better visibility
                new androidx.appcompat.app.AlertDialog.Builder(MainActivity.this)
                        .setTitle("Connection Error")
                        .setMessage(userMessage)
                        .setPositiveButton("OK", null)
                        .show();
            }
        });
    }

    private void displayResult(PredictResponse.PredictData data) {
        cardResult.setVisibility(View.VISIBLE);

        tvPrediction.setText(data.prediction.toUpperCase());
        tvPrediction.setTextColor(data.prediction.equalsIgnoreCase("Spam") ? Color.RED : Color.parseColor("#43A047"));

        tvConfidence.setText("Confidence: " + data.confidencePercent);
        tvRisk.setText(data.riskLevel + " Risk");

        int riskColor;
        switch (data.riskLevel) {
            case "High":
                riskColor = Color.RED;
                break;
            case "Medium":
                riskColor = Color.parseColor("#FB8C00");
                break;
            case "Low":
            default:
                riskColor = Color.parseColor("#43A047");
                break;
        }
        tvRisk.getBackground().setTint(riskColor);

        cgKeywords.removeAllViews();
        if (data.detectedKeywords != null && !data.detectedKeywords.isEmpty()) {
            for (String kw : data.detectedKeywords) {
                Chip chip = new Chip(this);
                chip.setText(kw);
                chip.setChipBackgroundColorResource(android.R.color.transparent);
                chip.setChipStrokeWidth(2f);
                chip.setChipStrokeColorResource(R.color.grey_light);
                cgKeywords.addView(chip);
            }
        } else {
            Chip chip = new Chip(this);
            chip.setText("General Patterns");
            chip.setChipBackgroundColorResource(android.R.color.transparent);
            chip.setChipStrokeWidth(2f);
            chip.setChipStrokeColorResource(R.color.grey_light);
            cgKeywords.addView(chip);
        }

        // Display 4 Bullet Point Explanation
        LinearLayout layoutExplanation = findViewById(R.id.layoutExplanation);
        layoutExplanation.removeAllViews();
        if (data.explanation != null) {
            for (String point : data.explanation) {
                TextView bulletPoint = new TextView(this);
                bulletPoint.setText("• " + point);
                bulletPoint.setTextSize(14);
                bulletPoint.setPadding(0, 4, 0, 8);
                bulletPoint.setTextColor(getResources().getColor(R.color.text_secondary));
                layoutExplanation.addView(bulletPoint);
            }
        }

        cardResult.setAlpha(0f);
        cardResult.animate().alpha(1f).setDuration(500).start();
    }
}
