"""
Splits raw text into overlapping chunks for embedding.
Manual implementation — no third-party text splitter used.
"""




def chunk_text(chunk_size,overlap,text):
    text=text.strip()
    if isinstance(chunk_size,int) and isinstance(overlap,int):
        if chunk_size<0 or overlap<0:
            raise ValueError("only positive integers for chunksize and overlap")
        elif chunk_size<=overlap:
            raise ValueError("chunksize should be greater than overlap ")
        elif not text:
            raise ValueError("text is empty ")
        else:
            start=0
            chunks=[]
            while start<len(text):
                chunki=text[start:start+chunk_size]
                if len(chunki)<=overlap:
                    break
                chunks.append(chunki)
                start+=chunk_size-overlap
            return chunks
    else:
        raise TypeError("chunksize and overlap should be integers")