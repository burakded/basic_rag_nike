from transformers import pipeline, AutoTokenizer, BertForTokenClassification


def preprocess(text):
    noktalama_isaretleri = ['!', '?', '.', ',', '-', ':', ';', "'"]
    new_text = "".join(
        [char for char in text if char in noktalama_isaretleri or char.isalnum() or char.isspace()])
    new_text_Pure = "".join([char for char in text if char.isalnum(
    ) or char.isspace() or char == "'" or char == "-"])
    new_text_Pure = new_text_Pure.replace("'", " ").replace("-", " ")
    new_text = new_text_Pure.replace("I", "ı").lower()
    return new_text


def end2end(sent, capitalization_corr, punc_corr):

    p_sent = preprocess(sent)

    r1 = capitalization_corr(p_sent)
    r2 = punc_corr(p_sent)

    tokenized_sent = tokenizer.tokenize(p_sent)

    final_sent = ''

    i = 0

    while i < len(tokenized_sent):
        token = tokenized_sent[i]
        if r1[i]['entity'] == 'one':
            token = token.capitalize()
        elif r1[i]['entity'] == 'cap':
            token = token.upper()
            while tokenized_sent[i+1].startswith("##"):
                token += tokenized_sent[i+1][2:].upper()
                i += 1

        if r2[i]['entity'] != 'non':
            token += r2[i]['entity']

        if r2[i]['entity'] != "'":
            token += ' '

        final_sent += token
        i += 1

    final_sent = final_sent.replace(' ##', '')

    # print(final_sent)

    return final_sent


cap_model = BertForTokenClassification.from_pretrained(
    "ytu-ce-cosmos/turkish-base-bert-capitalization-correction")
punc_model = BertForTokenClassification.from_pretrained(
    "ytu-ce-cosmos/turkish-base-bert-punctuation-correction")

tokenizer = AutoTokenizer.from_pretrained(
    "turkish-base-bert-capitalization-correction")


capitalization_corr = pipeline("ner", model=cap_model, tokenizer=tokenizer)
punc_corr = pipeline("ner", model=punc_model, tokenizer=tokenizer)

# sent = "toplantı saat 9 da başlayacak ancak çoğu kişi gecikebilir"

sent = """
geçen hafta sonu arkadaşlarımla birlikte kısa bir tatile çıktık cuma akşamı yola çıktık yolculuk oldukça keyifli geçti cumartesi sabahı otele vardık odalarımıza yerleştikten sonra kahvaltıya indik kahvaltıda birçok seçenek vardı omlet simit taze sıkılmış portakal suyu ve çeşitli peynirler kahvaltıdan sonra sahile gitmeye karar verdik deniz çok sakindi ve hava mükemmeldi denizde yüzdük kumda yürüdük ve güneşlendik öğleden sonra şehri gezmeye çıktık tarihi yerleri ziyaret ettik ve bol bol fotoğraf çektik akşam yemeği için meşhur bir restorana gittik deniz ürünleri gerçekten çok tazeydi yemek sonrası otele döndüğümüzde çok yorgunduk ama tatilin ilk günü harika geçmişti pazar sabahı erken kalkıp bir doğa yürüyüşüne çıktık orman içinde yürümek çok huzur vericiydi dönüş yolunda biraz trafik vardı ama bu güzel tatilin ardından hiçbiri moralimizi bozamazdı eve vardığımızda herkes mutlu ve huzurluydu bir sonraki tatili planlamaya başladık bile
"""

print(end2end(sent, capitalization_corr, punc_corr))
# Geçen hafta sonu arkadaşlarımla birlikte kısa bir tatile çıktık. Cuma akşamı yola çıktık. Yolculuk oldukça keyifli geçti. Cumartesi sabahı otele vardık. Odalarımıza yerleştikten sonra kahvaltıya indik. Kahvaltıda birçok seçenek vardı; omlet, simit, taze sıkılmış portakal suyu ve çeşitli peynirler. Kahvaltıdan sonra sahile gitmeye karar verdik. Deniz çok sakindi ve hava mükemmeldi. Denizde yüzdük, kumda yürüdük ve güneşlendik. Öğleden sonra şehri gezmeye çıktık. Tarihi yerleri ziyaret ettik ve bol bol fotoğraf çektik. Akşam yemeği için meşhur bir restorana gittik. Deniz ürünleri gerçekten çok tazeydi. Yemek sonrası otele döndüğümüzde çok yorgunduk ama tatilin ilk günü harika geçmişti. Pazar sabahı erken kalkıp bir doğa yürüyüşüne çıktık. Orman içinde yürümek çok huzur vericiydi. Dönüş yolunda biraz trafik vardı ama bu güzel tatilin ardından hiçbiri moralimizi bozamazdı. Eve vardığımızda herkes mutlu ve huzurluydu. Bir sonraki tatili planlamaya başladık bile.

