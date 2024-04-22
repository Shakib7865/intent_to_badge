
import streamlit as st


cnx=st.connection("snowflake")
session = cnx.session()

if "link_row_exists" not in st.session_state:
   st.session_state['link_row_exists']=False

def get_user_workshop_acct_info(current_interest):
   # get a table of all the entries this user has made
   workshop_sql =  (f"select award_desc, ACCOUNT_IDENTIFIER, account_locator " 
                     f"from AMAZING.APP.USER_LINK_ROWS where UNI_ID=trim('{st.session_state.uni_id}') " 
                     f"and UNI_UUID=trim('{st.session_state.uni_uuid}') and award_desc like '%" +current_interest+ "%' ") 
   workshop_df = session.sql(workshop_sql)
   workshop_results = workshop_df.to_pandas()
   row_exists = workshop_results.shape[0]
   if row_exists == 0:
      st.session_state.link_row_exists = False
   else: 
      st.session_state.link_row_exists = True
   st.write("Your Link row for " + current_interest+ ":")
   st.dataframe(workshops_results, hide_index=True)
   

st.subheader(":white_check_mark: Badge Requirements")
st.write("Please check the requirements listed on this page. We get SO MANY inquiries that we should not get. This app should provide you with what you need to SELF-SERVICE any issues.")

st.write("This app is new as of April 9th, 2024. You may have used other methods to get badges in the past. The concepts are the same but the methods have changed.")
st.markdown('----------')

if 'auth_status' not in st.session_state or st.session_state.auth_status == 'not_authed': 
   st.markdown(":red[Please sign in using your UNI_ID and UUID in the sidebar of the homepage.]")

elif st.session_state.auth_status == 'authed':
   if st.session_state.link_row_exists == False:
     emoji_1 = ":x:"  
   else:
     emoji_1 = ":white_check_mark:"
   label_1 =  "**CURRENT STATUS:** Your name is listed as :blue[" + st.session_state.given_name + " " + st.session_state.middle_name + " " + st.session_state.family_name +"]"
   st.markdown(emoji_1 + " **STEP 1:** Tell us your name and email.") 
   st.markdown(label_1)
   st.markdown("*Edit as needed. This is done on the :pencil2:  page.*") 

   st.markdown('----------')


   if "DISPLAY NAME" in st.session_state.display_name:
     emoji_2 = ":x:"
     label_2 = ":red[YOU HAVE NOT GENERATED A DISPLAY NAME FOR YOUR BADGE]"
   else:
     emoji_2 = ":white_check_mark:"
     label_2 = "**YOU CHOSE DISPLAY NAME: ** :green[" + st.session_state.display_name + "]"
  
   st.markdown(emoji_2 + " **STEP 2:** Generate a Display Name. :green[This is NEW!]") 
   st.markdown(label_2)
   st.markdown("*The Display Name feature gives you full control over how your name is displayed on any badge that is issued. This is done on the :star: page.*") 
   st.markdown("")
   
   st.markdown('------------')

   st.subheader("Repeat Steps 3 & 4 For EVERY NEW BADGE You Pursue")
   current_interest=st.selectbox("I want to check my status for:", ("DWW","CMCW", "DABW", "DLKW", "DNGW"))
   st.markdown('---------------------')

   if st.session_state.given_name is None:
     emoji_3 = ":x:"  
   else:
     emoji_3 = ":white_check_mark:"
   st.markdown(":white_check_mark: **STEP 3:** For EVERY BADGE you hope to receive, you will need to see a row on the :chains: page.") 
   get_user_workshop_acct_info(current_interest)
   st.markdown("To create or edit the info on the :chains: page, use the :link: page. Without this LINK established for each badge, DORA does not know who is doing the work so she cannot issue the badge.")         
   st.markdown("Every badge entry on the :chains: page should have both Account Locator and Account ID field completed.")
   st.markdown("")
   st.markdown("*Some older entries where you have already received your badge may have empty values. That is okay for older badges but for NEW badges, ALL columns MUST be complete.*")



   st.markdown('---------------------')
   st.markdown(":white_check_mark: **STEP 4:** For EVERY BADGE you hope to recieve, you need to complete every DORA check and see both PASSED and VALID for that test.") 
   st.markdown("*View your tests on the :robot_face: page. Filter down to PASSED and VALID. These are the only tests DORA considers.*")
   st.markdown("*A test that is PASSED but NOT VALID is a test that was changed by you before sending it to DORA.*")
   st.markdown("*You can FAIL any or all tests many times as long as you pass each test at least one time (and it is valid). When each test has at least one VALID/PASSED entry you can receive your badge.*")

   st.markdown('---------------------')

   st.subheader(":x: Troubleshooting")
   st.markdown("Did you make one of these common mistakes?")
   st.markdown(":x: Have you received this badge already? We check the UNI ID before issueing. We don't issue twice to the same UNI ID.")
   st.markdown(":x: Has someone using the same Snowflake Trial Account already received the badge? We don't issue twice on the same Trial Account.")
   st.markdown(":x: Did you accidently skip a test? Look closely at your tests, is any number in the sequence missing?")
   st.markdown(":x: Did mis-spell your email? It happens so often. If you did this, you'll have to file a ticket to get it corrected.")
   st.markdown(":x: Have you checked ACHIEVE.SNOWFLAKE.COM and/or your Email Inbox to see if your badge was already issued? The :sports_medal: page has some lag time between when your badge is issued and when it shows up in that list.")

else:
   st.markdown(":red[Please sign in using your UNI_ID and UUID in the sidebar of the homepage.]")

