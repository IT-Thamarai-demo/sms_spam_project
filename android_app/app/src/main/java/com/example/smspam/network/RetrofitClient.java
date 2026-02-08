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
    // - For EMULATOR: Use "http://10.0.2.2:5000/"
    // - For PHYSICAL DEVICE: Use your PC's IP (e.g., "http://192.168.1.10:5000/")
    // Find PC IP: Open CMD -> type 'ipconfig' -> find IPv4 Address

    // Change this to your PC's actual IPv4 address
    // Your PC IP: 10.18.234.93 (from ipconfig)
    private static final String BASE_URL = "http://10.18.234.93:5000/";

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
