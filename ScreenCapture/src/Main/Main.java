package Main;

import java.awt.AWTException;
import java.awt.Graphics2D;
import java.awt.HeadlessException;
import java.awt.Rectangle;
import java.awt.RenderingHints;
import java.awt.Robot;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

import javax.imageio.ImageIO;

import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import org.jnativehook.keyboard.NativeKeyEvent;
import org.jnativehook.keyboard.NativeKeyListener;

public class Main {
	static Timer timer;
	static int index = 0;
	static ArrayList<ArrayList<String>> names;
	static boolean film;
	static int key;
	static Robot robot;

	public static void main(String[] args) {
		try {
			robot = new Robot();
		} catch (AWTException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		try {
			GlobalScreen.registerNativeHook();
		} catch (NativeHookException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		GlobalScreen.addNativeKeyListener(new NativeKeyListener() {

			@Override
			public void nativeKeyTyped(NativeKeyEvent arg0) {

			}

			@Override
			public void nativeKeyReleased(NativeKeyEvent arg0) {
				if (arg0.getKeyCode() == NativeKeyEvent.VC_SPACE) {
					film = false;
				}
				if (arg0.getKeyCode() == NativeKeyEvent.VC_LEFT || arg0.getKeyCode() == NativeKeyEvent.VC_RIGHT) {
					key = 1;
				}
				if (arg0.getKeyCode() == NativeKeyEvent.VC_ENTER) {
					for (int i = 0; i < 3; i++) {
						try {
							PrintWriter save = new PrintWriter("Data " + i + ".txt");
							for (int j = 0; j < names.get(i).size(); j++) {
								save.println(names.get(i).get(j));
							}
							save.close();
						} catch (FileNotFoundException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
					}
				}
			}

			@Override
			public void nativeKeyPressed(NativeKeyEvent arg0) {
				if (arg0.getKeyCode() == NativeKeyEvent.VC_SPACE) {
					film = true;
				}
				if (arg0.getKeyCode() == NativeKeyEvent.VC_LEFT) {
					key = 0;
				}
				if (arg0.getKeyCode() == NativeKeyEvent.VC_RIGHT) {
					key = 2;
				}
			}
		});

		names = new ArrayList<ArrayList<String>>();
		names.add(new ArrayList<String>());
		names.add(new ArrayList<String>());
		names.add(new ArrayList<String>());

		timer = new Timer();
		timer.scheduleAtFixedRate(new TimerTask() {

			@Override
			public void run() {
				if (film) {
					BufferedImage image = null;
					try {
						image = robot.createScreenCapture(new Rectangle(540, 390, 785, 495));
					} catch (HeadlessException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					image = scaleImage(image, BufferedImage.TYPE_INT_RGB, 157, 99);
					try {
						ImageIO.write(image, "png", new File("data/" + index + ".png"));
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					names.get(key).add(index + ".png");
					index++;
				}
			}
		}, 0, 10);

	}
	public static BufferedImage scaleImage(BufferedImage image, int imageType,
	        int newWidth, int newHeight) {
	        // Make sure the aspect ratio is maintained, so the image is not distorted
	        double thumbRatio = (double) newWidth / (double) newHeight;
	        int imageWidth = image.getWidth(null);
	        int imageHeight = image.getHeight(null);
	        double aspectRatio = (double) imageWidth / (double) imageHeight;

	        if (thumbRatio < aspectRatio) {
	            newHeight = (int) (newWidth / aspectRatio);
	        } else {
	            newWidth = (int) (newHeight * aspectRatio);
	        }

	        // Draw the scaled image
	        BufferedImage newImage = new BufferedImage(newWidth, newHeight,
	                imageType);
	        Graphics2D graphics2D = newImage.createGraphics();
	        graphics2D.setRenderingHint(RenderingHints.KEY_INTERPOLATION,
	            RenderingHints.VALUE_INTERPOLATION_BILINEAR);
	        graphics2D.drawImage(image, 0, 0, newWidth, newHeight, null);

	        return newImage;
	    }

}
