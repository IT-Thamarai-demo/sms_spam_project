package com.example.smspam.network;

import android.util.Log;
import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitClient {
    private static final String TAG = "SMS_SPAM_API";
    private static Retrofit retrofit = null;

    // IMPORTANT: Network Configuration
    // - For EMULATOR: Use "http://10.0.2.2:5000/" (maps to localhost on your PC)
    // - For PHYSICAL DEVICE: Use your PC's actual IP address, e.g.,
    // "http://192.168.1.100:5000/"
    // Find your PC IP with: ipconfig (Windows) or ifconfig (Mac/Linux)
    // Make sure PC firewall allows port 5000

    // CONFIGURED FOR: Physical Device (PC IP: 10.173.3.93)
    private static final String BASE_URL = "http://10.173.3.93:5000/";

    public static ApiService getService() {
        if (retrofit == null) {
            Log.d(TAG, "Initializing Retrofit with BASE_URL: " + BASE_URL);

            // Add logging interceptor to see network requests/responses
            HttpLoggingInterceptor loggingInterceptor = new HttpLoggingInterceptor(
                    message -> Log.d(TAG, "HTTP: " + message));
            loggingInterceptor.setLevel(HttpLoggingInterceptor.Level.BODY);

            OkHttpClient client = new OkHttpClient.Builder()
                    .addInterceptor(loggingInterceptor)
                    .build();

            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .client(client)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit.create(ApiService.class);
    }
}
