package com.example.smspam;

import android.database.Cursor;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
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
        List<HistoryAdapter.HistoryItem> historyList = new ArrayList<>();
        Cursor cursor = dbHelper.getAllHistory();

        if (cursor != null && cursor.moveToFirst()) {
            do {
                String msg = cursor.getString(cursor.getColumnIndexOrThrow("message_text"));
                String pred = cursor.getString(cursor.getColumnIndexOrThrow("prediction"));
                String conf = cursor.getString(cursor.getColumnIndexOrThrow("confidence_percent"));
                String time = cursor.getString(cursor.getColumnIndexOrThrow("timestamp"));
                historyList.add(new HistoryAdapter.HistoryItem(msg, pred, conf, time));
            } while (cursor.moveToNext());
            cursor.close();
        }

        if (historyList.isEmpty()) {
            tvNoHistory.setVisibility(View.VISIBLE);
            rvHistory.setVisibility(View.GONE);
        } else {
            tvNoHistory.setVisibility(View.GONE);
            rvHistory.setVisibility(View.VISIBLE);
            rvHistory.setAdapter(new HistoryAdapter(historyList));
        }
    }
}
