package com.example.smspam;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.List;

public class HistoryAdapter extends RecyclerView.Adapter<HistoryAdapter.ViewHolder> {

    private final List<HistoryItem> historyList;

    public HistoryAdapter(List<HistoryItem> historyList) {
        this.historyList = historyList;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_history, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        HistoryItem item = historyList.get(position);
        holder.tvMessage.setText(item.message);
        holder.tvPrediction.setText(item.prediction.toUpperCase());
        holder.tvConfidence.setText("Confidence: " + item.confidence);
        holder.tvTime.setText(item.timestamp);

        int statusColor = item.prediction.equalsIgnoreCase("Spam") ? Color.RED : Color.parseColor("#43A047");
        holder.viewIndicator.setBackgroundColor(statusColor);
        holder.tvPrediction.setTextColor(statusColor);
    }

    @Override
    public int getItemCount() {
        return historyList.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvMessage, tvPrediction, tvConfidence, tvTime;
        View viewIndicator;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            tvMessage = itemView.findViewById(R.id.tvMessage);
            tvPrediction = itemView.findViewById(R.id.tvPrediction);
            tvConfidence = itemView.findViewById(R.id.tvConfidence);
            tvTime = itemView.findViewById(R.id.tvTime);
            viewIndicator = itemView.findViewById(R.id.viewIndicator);
        }
    }

    public static class HistoryItem {
        String message, prediction, confidence, timestamp;

        public HistoryItem(String message, String prediction, String confidence, String timestamp) {
            this.message = message;
            this.prediction = prediction;
            this.confidence = confidence;
            this.timestamp = timestamp;
        }
    }
}
