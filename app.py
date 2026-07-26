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

        if label.lower() == "positive":
            st.success("😊 Positive sentiment detected")
        elif label.lower() == "neutral":
            st.info("😐 Neutral sentiment detected")
        else:
            st.error("😞 Negative sentiment detected")

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
            normalized_columns = {col.lower().strip(): col for col in df.columns}
            preferred_candidates = [
                "review",
                "review_text",
                "reviewtext",
                "text",
                "feedback",
                "comments",
                "comment",
                "summary",
            ]

            review_column = None
            for candidate in preferred_candidates:
                if candidate in normalized_columns:
                    review_column = normalized_columns[candidate]
                    break

            if review_column is None:
                st.warning(
                    "Could not find a recognizable text column automatically. Please select one from the dropdown below."
                )
                review_column = st.selectbox("Select the text column to analyze", df.columns)

            if review_column is not None:
                reviews = df[review_column].fillna("").astype(str).tolist()
                non_empty_indices = [index for index, review in enumerate(reviews) if review.strip()]
                non_empty_reviews = [reviews[index] for index in non_empty_indices]

                if not non_empty_reviews:
                    st.info("The selected text column does not contain any non-empty values.")
                else:
                    st.write(f"Total reviews: {len(non_empty_reviews)}")

                    batch_size = 200
                    predictions = []
                    progress_text = st.empty()
                    progress_bar = st.progress(0)

                    for start in range(0, len(non_empty_reviews), batch_size):
                        batch = non_empty_reviews[start : start + batch_size]
                        batch_number = start // batch_size + 1
                        total_batches = (len(non_empty_reviews) + batch_size - 1) // batch_size

                        progress_text.text(
                            f"Analyzing batch {batch_number} of {total_batches} ({min(start + batch_size, len(non_empty_reviews))}/{len(non_empty_reviews)} reviews)"
                        )

                        with st.spinner("Analyzing reviews..."):
                            batch_predictions = analyze_sentiment_batch(batch)

                        predictions.extend(batch_predictions)
                        progress_value = min((start + len(batch)) / len(non_empty_reviews), 1.0)
                        progress_bar.progress(progress_value)

                    progress_text.text("Analysis complete")
                    progress_bar.progress(1.0)

                    df["sentiment"] = ""
                    df["confidence"] = ""

                    for row_index, prediction in zip(non_empty_indices, predictions):
                        df.at[row_index, "sentiment"] = prediction["label"]
                        df.at[row_index, "confidence"] = f"{prediction['confidence']}%"

                    st.dataframe(df)

                    positive_count = int((df["sentiment"].str.lower() == "positive").sum())
                    neutral_count = int((df["sentiment"].str.lower() == "neutral").sum())
                    negative_count = int((df["sentiment"].str.lower() == "negative").sum())
                    total_reviews = len(df)

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total reviews", total_reviews)
                    col2.metric("Positive reviews", positive_count)
                    col3.metric("Neutral reviews", neutral_count)
                    col4.metric("Negative reviews", negative_count)

                    summary_df = pd.DataFrame(
                        {
                            "Sentiment": ["Positive", "Neutral", "Negative"],
                            "Count": [positive_count, neutral_count, negative_count],
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
