package com.example.findyourngo

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.snackbar.Snackbar
import kotlinx.android.synthetic.main.activity_basic.*
import okhttp3.Credentials
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response

class BasicActivity : AppCompatActivity() {
    // https://stackoverflow.com/questions/45219379/how-to-make-an-api-request-in-kotlin
    // https://square.github.io/okhttp/recipes/

    private val client = OkHttpClient()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_basic)
        setSupportActionBar(toolbar)

        fab.setOnClickListener { view ->
            Snackbar.make(view, "Get result: " + run("http://10.0.2.2:8000/users/?format=json"), Snackbar.LENGTH_LONG)
                .setAction("Action", null).show()
        }
    }

    private fun run(url: String): String {
        val request = Request.Builder()
            .url(url)
            .header("Authorization", Credentials.basic("admin", "password123"))
            .build()

        /* An async call example
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {}
            override fun onResponse(call: Call, response: Response) = println(response.body()?.string())
        })
        */
        var result: Response? = null
        val thread = Thread(Runnable {result = client.newCall(request).execute()})
        thread.start()
        thread.join()

        return result?.body()!!.string()
    }

}
