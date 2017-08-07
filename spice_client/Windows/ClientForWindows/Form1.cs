using System;
using System.Windows.Forms;
using System.Diagnostics;


namespace ClientForWindows
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            VisiblePassword.Checked = false;
            Password.UseSystemPasswordChar = true;
           
        }

        private void Password_TextChanged(object sender, EventArgs e)
        {

        }

        private void Login_TextChanged(object sender, EventArgs e)
        {

        }

        private void LogInBtn_Click(object sender, EventArgs e)
        {
            if (Login.Text == "")
            {
                MessageBox.Show("Не указан логин");
                return;
            }
            if (Password.Text == "")
            {
                MessageBox.Show("Не указан пароль");
                return;
            }

            string link = string.Empty;
            Exception check = Client.MakeConnection(Login.Text, Password.Text, out link);
            if (check != null)
            {
                MessageBox.Show(check.ToString());
                return;
            }
            if (link == string.Empty)
            {
                MessageBox.Show("Отсутствует VM с указанными логином и паролем!", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            System.Uri uri;
            if (!Uri.TryCreate(link, UriKind.Absolute, out uri))
            {
                MessageBox.Show(link, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            Process.Start(link);
           
        }

        private void VisiblePassword_CheckedChanged(object sender, EventArgs e)
        {
            Password.UseSystemPasswordChar = !Password.UseSystemPasswordChar;
        }
    }
}
