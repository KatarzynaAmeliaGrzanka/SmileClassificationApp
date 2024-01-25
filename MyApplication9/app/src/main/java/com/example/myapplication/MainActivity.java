package com.example.myapplication;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.media.ThumbnailUtils;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Mat;
import org.opencv.core.MatOfRect;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.core.CvType;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;


import com.example.myapplication.ml.Model2;
import com.example.myapplication.ml.ModelSmileClassify;


import org.tensorflow.lite.DataType;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;



public class MainActivity extends AppCompatActivity {

    static {
        if(OpenCVLoader.initDebug()){
            Log.d("MainActivity: ","Opencv is loaded");
        }
        else {
            Log.d("MainActivity: ","Opencv failed to load");
        }
    }
    Button camera_btn, gallery_btn;
    TextView result_view, result_spontaneity;
    ImageView imageView;
    private static CascadeClassifier cascadeClassifier;
    private CascadeClassifier cascadeClassifierEyes;

    int image_size = 256;
   ;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        camera_btn = findViewById((R.id.button));
        gallery_btn = findViewById((R.id.button2));
        result_view = findViewById((R.id.result));
        imageView = findViewById((R.id.imageView));
        result_spontaneity = findViewById((R.id.result_spontaneity));


        //Interface definition for a callback to be invoked when a view is clicked.
        camera_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                    Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                    startActivityForResult(cameraIntent, 3);
                } else {
                    requestPermissions(new String[]{Manifest.permission.CAMERA}, 100);
                }
            }
        });
        //Interface definition for a callback to be invoked when a view is clicked.
        gallery_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent cameraIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                startActivityForResult(cameraIntent, 1);
            }
        });

        try{
            InputStream is = getResources().openRawResource(R.raw.haarcascade_frontalface_alt);
            File cascadeDir = getDir("cascade", Context.MODE_PRIVATE);
            File mCascadeFile = new File(cascadeDir, "haarcascade_frontalface_alt.xml");
            FileOutputStream os = new FileOutputStream(mCascadeFile);
            byte[] buffer = new byte[4096];
            int byteRead;
            while ((byteRead = is.read(buffer)) != -1){
                os.write(buffer, 0, byteRead);
            }
            is.close();
            os.close();

            cascadeClassifier = new CascadeClassifier(mCascadeFile.getAbsolutePath());
            // model loaded

        } catch (IOException e) {
            e.printStackTrace();
        }

        try{
            InputStream is = getResources().openRawResource(R.raw.haarcascade_eye_tree_eyeglasses);
            File cascadeDir = getDir("cascade", Context.MODE_PRIVATE);
            File mCascadeFile = new File(cascadeDir, "haarcascade_eye_tree_eyeglasses.xml");
            FileOutputStream os = new FileOutputStream(mCascadeFile);
            byte[] buffer = new byte[4096];
            int byteRead;
            while ((byteRead = is.read(buffer)) != -1){
                os.write(buffer, 0, byteRead);
            }
            is.close();
            os.close();

            cascadeClassifierEyes = new CascadeClassifier(mCascadeFile.getAbsolutePath());
            // model loaded

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public Bitmap allign_face(Bitmap image){
        Mat mRgba = new Mat(image.getHeight(), image.getWidth(), CvType.CV_8UC4);
        Utils.bitmapToMat(image, mRgba);

        Mat mRbg = new Mat();
        Imgproc.cvtColor(mRgba, mRbg, Imgproc.COLOR_RGBA2RGB);

        int height = mRbg.height();
        int absoluteFaceSize = (int) (height * 0.001);

        MatOfRect eyes = new MatOfRect();
        if (cascadeClassifierEyes != null) {
            cascadeClassifierEyes.detectMultiScale(mRbg, eyes, 1.1, 2, 2, new Size(absoluteFaceSize, absoluteFaceSize), new Size());
        }

        Bitmap AlignedFace = null;
        Rect[] eyesArray = eyes.toArray();

        if (eyesArray.length == 2){
            Point eye1 = new Point(eyesArray[0].x, eyesArray[0].y );
            Point eye2 = new Point(eyesArray[1].x, eyesArray[1].y );

            double angle = Math.atan2(eye2.y - eye1.y, eye2.x - eye1.x);
            double degreeAngle = Math.toDegrees(angle);

            if (degreeAngle > 90){
                angle = Math.atan2(eye1.y - eye2.y, eye1.x - eye2.x);
                degreeAngle = Math.toDegrees(angle);
            }

            Mat rotatedMat = Imgproc.getRotationMatrix2D(new Point(mRbg.cols() / 2, mRbg.rows() / 2), degreeAngle, 1);
            Mat alignedFaceMat = new Mat();
            Imgproc.warpAffine(mRbg, alignedFaceMat, rotatedMat, mRbg.size());

            Bitmap alignedFace = Bitmap.createBitmap(alignedFaceMat.cols(), alignedFaceMat.rows(), Bitmap.Config.ARGB_8888);
            Utils.matToBitmap(alignedFaceMat, alignedFace);

            return alignedFace;
        }
        else{
            Log.d("FaceDetection", "Wrong number of eyes detected");
        }

        return  image;
    }

    public static Bitmap detect_face(Bitmap image) {
        if (image == null){
            return null;
        }

        Mat mRgba = new Mat(image.getHeight(), image.getWidth(), CvType.CV_8UC4);
        Utils.bitmapToMat(image, mRgba);

        Mat mRbg = new Mat();
        Imgproc.cvtColor(mRgba, mRbg, Imgproc.COLOR_RGBA2RGB);

        int height = mRbg.height();
        int absoluteFaceSize = (int) (height * 0.1);

        MatOfRect faces = new MatOfRect();
        if (cascadeClassifier != null) {
            cascadeClassifier.detectMultiScale(mRbg, faces, 1.1, 2, 2, new Size(absoluteFaceSize, absoluteFaceSize), new Size());
        }
        Log.d("FaceDetection", "Number of faces detected: " + faces.toArray().length);
        Bitmap croppedFace = null;
        Rect[] facesArray = faces.toArray();
        if (facesArray.length > 0) {
            Rect firstFace = facesArray[0];

            // Crop the image to the detected face region
            Mat croppedMat = new Mat(mRgba, firstFace);
            croppedFace = Bitmap.createBitmap(croppedMat.cols(), croppedMat.rows(), Bitmap.Config.ARGB_8888);
            Utils.matToBitmap(croppedMat, croppedFace);

            // Draw a rectangle around the detected face on the original image
            Imgproc.rectangle(mRgba, firstFace.tl(), firstFace.br(), new Scalar(0, 255, 0, 255), 2);
            Bitmap resultBitmap = Bitmap.createBitmap(mRgba.cols(), mRgba.rows(), Bitmap.Config.ARGB_8888);

            Utils.matToBitmap(mRgba, resultBitmap);
            //imageView.setImageBitmap(resultBitmap);
            return croppedFace;

        } else {
            return image;
        }
    }

    public void classifyImage(Bitmap image){
        try {
            Bitmap image_tmp = image;
            image = detect_face(image);
            image =  allign_face(image);

            if (image == image_tmp){
                imageView.setImageBitmap(image_tmp);
                result_view.setText("No face detected.");
                result_spontaneity.setText("0");
            }

            else{
                imageView.setImageBitmap(image);

                ModelSmileClassify model = ModelSmileClassify.newInstance(getApplicationContext());

                // Creates inputs for reference.
                TensorBuffer inputFeature0 = TensorBuffer.createFixedSize(new int[]{1, 256 , 256, 3}, DataType.FLOAT32);

                ByteBuffer byteBuffer = ByteBuffer.allocateDirect( 4 * image_size * image_size * 3);
                byteBuffer.order(ByteOrder.nativeOrder());

                int[] intValues = new int[image_size * image_size];
                image.getPixels(intValues, 0, image.getWidth(), 0, 0, image.getWidth(), image.getHeight());
                int pixel = 0;

                for(int i = 0; i < image_size; i ++) {
                    for (int j = 0; j < image_size; j++) {
                        int val = intValues[pixel++]; // RGB
                        byteBuffer.putFloat(((val >> 16) & 0xFF) * (1.f));
                        byteBuffer.putFloat(((val >> 8) & 0xFF) * (1.f));
                        byteBuffer.putFloat((val & 0xFF) * (1.f));
                    }
                }
                inputFeature0.loadBuffer(byteBuffer);


                ModelSmileClassify.Outputs outputs = model.process(inputFeature0);
                TensorBuffer outputFeature0 = outputs.getOutputFeature0AsTensorBuffer();

                float[] confidences = outputFeature0.getFloatArray();
                if (confidences[0] > 0.5){
                    result_view.setText("Spontaneous");
                } else{
                    result_view.setText("Deliberate");
                }

                String stringValue = String.valueOf(confidences[0]);
                result_spontaneity.setText(stringValue);


                model.close();
            }

        } catch (IOException e) {
        }

    }



    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if (resultCode == RESULT_OK){
            // if image form camera

            if(requestCode == 3){
                Bitmap image = (Bitmap) data.getExtras().get("data");
                // dodać detekcje i normalizacje
                //image = detect_face(image);
                int dimension = Math.min(image.getWidth(), image.getHeight());
                image = ThumbnailUtils.extractThumbnail(image, dimension, dimension);
               // imageView.setImageBitmap(image);
                image = Bitmap.createScaledBitmap(image, image_size, image_size, false);
                classifyImage(image);
            }
            // if image form gallery
            else{
                Uri dat = data.getData();
                Bitmap image = null;
                try {
                    image = MediaStore.Images.Media.getBitmap(this.getContentResolver(), dat);

                } catch (IOException e) {
                    e.printStackTrace();
                }
               // imageView.setImageBitmap(image);

                image = Bitmap.createScaledBitmap(image, image_size, image_size, false);
                //image = detect_face(image);
                classifyImage(image);
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }
}