package by.manti.apollo;

import java.lang.Exception;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.os.AsyncTask;
import android.view.View;
import android.widget.TextView;
import android.app.AlertDialog;

import org.json.JSONObject;

import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;


public class MainActivity extends AppCompatActivity {

    private TextView tank_temp, column_temp, spirit_temp;
    private AlertDialog.Builder dialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        dialog = new AlertDialog.Builder(this);

        tank_temp = (TextView) findViewById(R.id.tank_temp);
        column_temp = (TextView) findViewById(R.id.column_temp);
        spirit_temp = (TextView) findViewById(R.id.spirit_temp);

        tank_temp.setText("0");
        column_temp.setText("0");
        spirit_temp.setText("0");
    }

    public void updateData(View v) {
        new LongOperation().execute("http://rpi/api?latest=1");
    }

    private class LongOperation extends AsyncTask<String, Void, Void> {

        private final HttpClient Client = new DefaultHttpClient();
        private String Content;

        @Override
        protected Void doInBackground(String... params) {
            try {
                HttpGet httpget = new HttpGet(params[0]);
                ResponseHandler<String> responseHandler = new BasicResponseHandler();
                Content = Client.execute(httpget, responseHandler);
            } catch (Exception e) {
                dialog.setTitle("Error");
                dialog.setMessage(e.getMessage());
                cancel(true);
            }
            return null;
        }

        @Override
        protected void onPreExecute() {
        }

        @Override
        protected void onProgressUpdate(Void... values) {
        }

        protected void onPostExecute(Void unused) {
            try {
                JSONObject response = new JSONObject(Content);

                if (response.getInt("status") == 200) {
                    JSONObject data = (JSONObject) response.get("data");

                    tank_temp.setText(data.getString("tank_temp"));
                    column_temp.setText(data.getString("column_temp"));
                    spirit_temp.setText(data.getString("spirit_temp"));
                } else {
                    dialog.setTitle("Error");
                    dialog.setMessage(response.getString("message"));
                }
            } catch (Exception e) {
                dialog.setTitle("Error");
                dialog.setMessage(e.getMessage());
            }
        }
    }
}
