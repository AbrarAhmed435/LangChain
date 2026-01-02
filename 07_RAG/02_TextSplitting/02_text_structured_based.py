from langchain_text_splitters import RecursiveCharacterTextSplitter


text='''Love is one of the most profound and complex emotions humans experience. It goes beyond simple attraction or affection; it is a deep connection that binds people through understanding, care, and commitment. Love can exist in many forms—romantic love, familial love, friendship, and even self-love—and each plays a vital role in shaping who we are.

At its core, love is about empathy and acceptance. It allows us to see another person not as perfect, but as real, with flaws, fears, and dreams. True love does not demand change; instead, it encourages growth while offering a sense of safety and belonging. When we love someone, we invest emotionally, choosing to support them not only in moments of happiness but also during times of struggle.

Love also requires effort and patience. Contrary to popular belief, it is not sustained by intense emotions alone. Over time, love evolves into trust, respect, and shared responsibility. Disagreements and misunderstandings are inevitable, but love teaches us how to communicate, forgive, and compromise. These moments test the strength of the bond and often deepen it.

Beyond personal relationships, love influences how we interact with the world. It fosters kindness, compassion, and a willingness to help others. Love has the power to heal emotional wounds, inspire creativity, and give life a sense of meaning. It motivates people to become better versions of themselves, not out of obligation, but out of care.

In a world often driven by speed and self-interest, love reminds us to slow down and connect. It is not always loud or dramatic; sometimes, love is found in quiet gestures—a listening ear, a shared silence, or unwavering support. Ultimately, love is not just something we feel; it is something we choose to practice every day.
'''

splitter=RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=0
)
chunks=splitter.split_text(text)

print(len(chunks))
print(chunks)