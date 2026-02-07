package com.example.smspam.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class DatabaseHelper extends SQLiteOpenHelper {
    private static final String DATABASE_NAME = "smspam.db";
    private static final int DATABASE_VERSION = 1;

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE history (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                "message_text TEXT, " +
                "prediction TEXT, " +
                "confidence_percent TEXT, " +
                "risk_level TEXT, " +
                "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS history");
        onCreate(db);
    }

    public void insertHistory(String msg, String pred, String conf, String risk) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put("message_text", msg);
        values.put("prediction", pred);
        values.put("confidence_percent", conf);
        values.put("risk_level", risk);
        db.insert("history", null, values);
    }

    public Cursor getAllHistory() {
        SQLiteDatabase db = this.getReadableDatabase();
        return db.rawQuery("SELECT * FROM history ORDER BY timestamp DESC", null);
    }
}
