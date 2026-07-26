import pandas as pd
import streamlit as st

from sentiment import analyze_sentiment, analyze_sentiment_batch


st.set_page_config(page_title="Customer Feedback Analyzer", page_icon="💬")
st.title("Customer Feedback Analyzer")
st.write("Enter one customer review and click Analyze.")

review = st.text_area(
    "Customer review",
    placeholder="Type a review here...",
    height=150,
)

if st.button("Analyze"):
    if review.strip():
        with st.spinner("Loading AI model..."):
            result = analyze_sentiment(review)

        label = result["label"]
        confidence = result["confidence"]

        st.subheader("Result")

        if label.lower().startswith("pos"):
            st.markdown(
                f"<div style='background-color:#e6f4ea; color:#1f7a1f; padding:12px; border-radius:8px;'>😊 Positive sentiment detected</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='background-color:#fdecea; color:#b42318; padding:12px; border-radius:8px;'>😞 Negative sentiment detected</div>",
                unsafe_allow_html=True,
            )

        st.markdown(f"**Confidence:** {confidence}%")
    else:
        st.warning("Please enter a review before clicking Analyze.")

st.divider()
st.subheader("Analyze multiple reviews")
st.write("Upload a CSV file with a review column to analyze several reviews at once.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if df.empty:
            st.info("The uploaded file is empty.")
        else:
            review_column = None
            for candidate in ["review", "text", "feedback", "comments"]:
                if candidate in df.columns:
                    review_column = candidate
                    break

            if review_column is None:
                st.warning(
                    "Could not find a review column. Please include one named 'review', 'text', 'feedback', or 'comments'."
                )
            else:
                reviews = df[review_column].fillna("").astype(str).tolist()
                non_empty_indices = [index for index, review in enumerate(reviews) if review.strip()]
                non_empty_reviews = [reviews[index] for index in non_empty_indices]

                if not non_empty_reviews:
                    st.info("The selected review column does not contain any non-empty values.")
                else:
                    with st.spinner("Analyzing all reviews..."):
                        predictions = analyze_sentiment_batch(non_empty_reviews)

                    df["sentiment"] = ""
                    df["confidence"] = ""
                    df.loc[non_empty_indices, "sentiment"] = [item["label"] for item in predictions]
                    df.loc[non_empty_indices, "confidence"] = [f"{item['confidence']}%" for item in predictions]

                    st.dataframe(df)

                    positive_count = int((df["sentiment"].str.lower().str.startswith("pos")).sum())
                    negative_count = int((df["sentiment"].str.lower().str.startswith("neg")).sum())
                    total_reviews = len(df)

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total reviews", total_reviews)
                    col2.metric("Positive reviews", positive_count)
                    col3.metric("Negative reviews", negative_count)

                    summary_df = pd.DataFrame(
                        {
                            "Sentiment": ["Positive", "Negative"],
                            "Count": [positive_count, negative_count],
                        }
                    )
                    st.bar_chart(summary_df.set_index("Sentiment"))

                    st.download_button(
                        label="Download analyzed CSV",
                        data=df.to_csv(index=False).encode("utf-8"),
                        file_name="analyzed_reviews.csv",
                        mime="text/csv",
                    )
    except Exception as exc:
        st.error(f"Could not process the file: {exc}")
