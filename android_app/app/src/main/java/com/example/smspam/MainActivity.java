package com.example.smspam;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
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
        if (msg.isEmpty())
            return;

        btnScan.setEnabled(false);
        btnScan.setText("Scanning...");

        ApiService service = RetrofitClient.getService();
        service.predict(new PredictRequest(msg)).enqueue(new Callback<PredictResponse>() {
            @Override
            public void onResponse(Call<PredictResponse> call, Response<PredictResponse> response) {
                btnScan.setEnabled(true);
                btnScan.setText(getString(R.string.btn_scan));

                if (response.isSuccessful() && response.body() != null && "success".equals(response.body().status)) {
                    PredictResponse.PredictData data = response.body().data;
                    displayResult(data);
                    dbHelper.insertHistory(msg, data.prediction, data.confidencePercent, data.riskLevel);
                } else {
                    String errorMsg = response.body() != null ? response.body().message : "Error from server";
                    Toast.makeText(MainActivity.this, errorMsg, Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<PredictResponse> call, Throwable t) {
                btnScan.setEnabled(true);
                btnScan.setText(getString(R.string.btn_scan));
                Toast.makeText(MainActivity.this, "Connection failed: " + t.getMessage(), Toast.LENGTH_LONG).show();
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
        if (data.detectedKeywords != null) {
            for (String kw : data.detectedKeywords) {
                Chip chip = new Chip(this);
                chip.setText(kw);
                chip.setChipBackgroundColorResource(android.R.color.transparent);
                chip.setChipStrokeWidth(2f);
                chip.setChipStrokeColorResource(R.color.grey_light);
                cgKeywords.addView(chip);
            }
        }
    }
}
