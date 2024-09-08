import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth

# Initialize Firebase app
cred = credentials.Certificate('pondering-tutorials-e54c6be2d468.json')
firebase_admin.initialize_app(cred)

def app():
    st.title("Welcome to :violet[Pondering] :sunglasses:")

    # Initialize session state variables if not already present
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ""
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    # Login function
    def login():
        email = st.session_state.email
        try:
            user = auth.get_user_by_email(email)
            st.success("Login successful!")
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signout = True
            st.session_state.signedout = True
        except Exception as e:
            st.warning(f'Login Failed: {e}')

    # Sign out function
    def sign_out():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ""
        st.session_state.useremail = ""

    # If user is signed out, show login/signup form
    if not st.session_state['signedout']:
        choose = st.selectbox('Login/Sign Up', ['Login', 'Sign Up'])

        if choose == "Login":
            st.session_state.email = st.text_input("Email Address:")
            password = st.text_input("Password", type='password')
            if st.button("Login", on_click=login):
                pass
        
        else:  # Sign Up section
            email = st.text_input("Email Address:")
            password = st.text_input("Password", type='password')
            username = st.text_input("Enter your unique username:")

            if st.button("Create my account"):
                try:
                    user = auth.create_user(
                        email=email,
                        password=password,
                        uid=username
                    )
                    st.success("Account created successfully!")
                    st.markdown("Please login using your email and password.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error creating account: {e}")

    # If the user is logged in, show user details and the sign out button
    if st.session_state.signout:
        st.text(f'Name: {st.session_state.username}')
        st.text(f'Email: {st.session_state.useremail}')
        st.button('Sign out', on_click=sign_out)

# Run the app
if __name__ == '__main__':
    app()
