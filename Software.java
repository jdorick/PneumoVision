import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.Color; 
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Software {
    public static void main(String[] args) {
        // Create the main window (JFrame)
        JFrame window = new JFrame("PneumoVision"); // Set the title
        window.setSize(300, 200);
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setLocationRelativeTo(null);  


        // Dark color aesthetic
        Color darkBackground = new Color(30, 30, 30); 
        window.getContentPane().setBackground(darkBackground); 

        JLabel label = new JLabel("Click the button");
        label.setForeground(Color.WHITE); // Contrasting text color

        JButton button = new JButton("Click Me!");
        button.setForeground(Color.WHITE); 
        button.setBackground(new Color(50, 50, 50));

        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                label.setText("Button clicked!");
                callPythonScript(); // Call the Python interaction
            }
        });

        window.add(label);
        window.add(button); 
        window.setVisible(true);
    }

    public static void callPythonScript() {
        try {
            Process p = Runtime.getRuntime().exec("CNN.py"); 

            // Read output from the Python script (placeholder)
            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String output;
            while ((output = reader.readLine()) != null) {
                System.out.println(output); 
            }

        } catch (Exception e) {
            // Handle exceptions
        }
    }
}
