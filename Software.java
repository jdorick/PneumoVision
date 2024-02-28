import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import javax.swing.filechooser.FileFilter;

public class Software {

	public static void main(String[] args) {
		SwingUtilities.invokeLater(() -> createAndShowGUI());
	}

	private static void createAndShowGUI() {
		JFrame window = new JFrame("PneumoVision");
		window.setSize(400, 300);
		window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		window.setLocationRelativeTo(null);

		setupUI(window);

		window.setVisible(true);
	}

	private static void setupUI(JFrame window) {
		// Use a layout manager (FlowLayout in this case)
		JPanel mainPanel = new JPanel(new BorderLayout());
		mainPanel.setBackground(new Color(30, 30, 30));

		// Header Label
		JLabel headerLabel = new JLabel("PneumoVision");
		headerLabel.setForeground(Color.WHITE);
		headerLabel.setFont(new Font("Arial", Font.BOLD, 28));
		headerLabel.setHorizontalAlignment(SwingConstants.CENTER);
		mainPanel.add(headerLabel, BorderLayout.NORTH);

		// Spacer
		mainPanel.add(Box.createRigidArea(new Dimension(0, 20)), BorderLayout.CENTER);

		// Upload Area
		JPanel uploadPanel = new JPanel(new BorderLayout());
		uploadPanel.setBackground(new Color(50, 50, 50));

		JLabel uploadLabel = new JLabel("Upload image from your computer");
		uploadLabel.setForeground(Color.WHITE);
		uploadLabel.setFont(new Font("Arial", Font.PLAIN, 18));
		uploadLabel.setHorizontalAlignment(SwingConstants.CENTER);
		uploadPanel.add(uploadLabel, BorderLayout.CENTER);

		JButton uploadButton = new JButton("Upload image from your computer");
		uploadButton.setForeground(Color.WHITE);
		uploadButton.setBackground(new Color(30, 144, 255)); // Customize the button color
		uploadButton.setFont(new Font("Arial", Font.PLAIN, 18));
		uploadButton.addActionListener(e -> handleUploadButton(window));
		uploadPanel.add(uploadButton, BorderLayout.CENTER);

		mainPanel.add(uploadPanel, BorderLayout.CENTER);

		window.getContentPane().add(mainPanel);
	}

	private static void handleUploadButton(JFrame window) {
		JFileChooser fileChooser = new JFileChooser();
		fileChooser.setAcceptAllFileFilterUsed(false);

		// Create a file filter that allows JPEG, PNG, and DICOM files
		FileFilter imageFilter = new FileFilter() {
			@Override
			public boolean accept(File file) {
				String fileName = file.getName().toLowerCase();
				return fileName.endsWith(".jpg") || fileName.endsWith(".jpeg")
						|| fileName.endsWith(".png") || fileName.endsWith(".dcm");
			}

			@Override
			public String getDescription() {
				return "Image Files (*.jpg, *.jpeg, *.png, *.dcm)";
			}
		};

		fileChooser.addChoosableFileFilter(imageFilter);

		if (fileChooser.showOpenDialog(window) == JFileChooser.APPROVE_OPTION) {
			File file = fileChooser.getSelectedFile();
			// Process the uploaded file (load into an image component)
			System.out.println("File selected: " + file.getAbsolutePath());
		}
	}
}

//		private static void callPythonScript() {
//			try {
//				Process p = Runtime.getRuntime().exec("python CNN.py");
//				BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
//				String output;
//				while ((output = reader.readLine()) != null) {
//					System.out.println(output);
//				}
//			} catch (Exception e) {
//				// Handle exceptions (log or display an error message)
//				e.printStackTrace();
//			}
//		}
