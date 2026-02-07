package com.example.smspam;

import android.database.Cursor;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.smspam.database.DatabaseHelper;
import java.util.ArrayList;
import java.util.List;

public class HistoryActivity extends AppCompatActivity {

    private RecyclerView rvHistory;
    private TextView tvNoHistory;
    private DatabaseHelper dbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);

        rvHistory = findViewById(R.id.rvHistory);
        tvNoHistory = findViewById(R.id.tvNoHistory);
        dbHelper = new DatabaseHelper(this);

        rvHistory.setLayoutManager(new LinearLayoutManager(this));
        loadHistory();

        findViewById(R.id.toolbar).setOnClickListener(v -> finish());
    }

    private void loadHistory() {
        android.util.Log.d("SMS_SPAM", "Loading history from database...");
        List<HistoryAdapter.HistoryItem> historyList = new ArrayList<>();
        Cursor cursor = null;

        try {
            cursor = dbHelper.getAllHistory();
            android.util.Log.d("SMS_SPAM", "Database query executed");

            if (cursor != null && cursor.moveToFirst()) {
                android.util.Log.d("SMS_SPAM", "Cursor has data, processing rows...");
                int count = 0;
                do {
                    String msg = cursor.getString(cursor.getColumnIndexOrThrow("message_text"));
                    String pred = cursor.getString(cursor.getColumnIndexOrThrow("prediction"));
                    String conf = cursor.getString(cursor.getColumnIndexOrThrow("confidence_percent"));
                    String time = cursor.getString(cursor.getColumnIndexOrThrow("timestamp"));
                    historyList.add(new HistoryAdapter.HistoryItem(msg, pred, conf, time));
                    count++;
                } while (cursor.moveToNext());
                android.util.Log.d("SMS_SPAM", "Loaded " + count + " history items from database");
            } else {
                android.util.Log.d("SMS_SPAM", "Cursor is empty or null");
            }
        } catch (Exception e) {
            android.util.Log.e("SMS_SPAM", "Error loading history: " + e.getMessage());
            e.printStackTrace();
            Toast.makeText(this, "Error loading history: " + e.getMessage(), Toast.LENGTH_LONG).show();
        } finally {
            if (cursor != null) {
                cursor.close();
            }
        }

        if (historyList.isEmpty()) {
            android.util.Log.d("SMS_SPAM", "History list is empty, showing 'No history' message");
            tvNoHistory.setVisibility(View.VISIBLE);
            rvHistory.setVisibility(View.GONE);
        } else {
            android.util.Log.d("SMS_SPAM", "Displaying " + historyList.size() + " history items");
            tvNoHistory.setVisibility(View.GONE);
            rvHistory.setVisibility(View.VISIBLE);
            rvHistory.setAdapter(new HistoryAdapter(historyList));
        }
    }
}
