# Unsupervised summarization algorithms

We apply two types of unsupervised algorithms:
* Domain-independent (RBM)
* Legal domain-specific (CaseSummarizer)

## Generated summaries

For the document [sample input.txt](../sample%20input.txt), we describe the summaries generated by each of the methods.

### RBM

```
python Summarizer.py sample_folder .

Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others Supreme Court of India  24 September 1953 Civil Appeal No.77 of 1952.The Judgment was delivered by : Mehr Chand Mahajan, J. 1.2.The assessee is a partnership concern.The name of the firm was A. W. Figgies & Co., and its' business was that of tea brokers.The Appellate Assistant Commissioner upheld this view.On appeal to the Income-tax Tribunal, this decision was reversed and relief was granted to the applicant under section 25(4).Before the Tribunal it was argued on behalf of the Commissioner that the partnership was nothing but an association of persons and therefore, in 24 174 order to get relief under section 25(4) of the Act the partners of 1939 must be the same as the partners of 1947 when the firm was succeeded by the company.It was not disputed before the Tribunal that the business of the partnership firm of A. W. Figgies & Co. continued as tea brokers right from its inception till the time it was succeeded by the limited company.The Tribunal took the view that for purposes of income tax the firm was to be regarded as having a separate juristic existence apart from the partners carrying on the business and that the firm could be carried on even if there was a change in its constitution.3.At the instance of the appellant the Tribunal stated a case and referred the following question to the High Court under section 66(1) of the Act : "In the facts and circumstances of the case, was the firm as constituted on 31st May, 1947, entitled to the relief under section 25(4) of the Indian Incometax Act "?4.The High Court answered the question referred in the affirmative.It upheld the view taken by the Tribunal.It was contended before us that the construction placed by the High Court upon section 25(4) of the Act was erroneous and was not warranted by the language of the section and that by reason of the change in the composition of the firm the same firm did not continue throughout and hence there was no right to relief under section 25(4) of the Act in the changed firm.In our opinion, this contention is without force.Section 25 (4) is in these terms:- "Where the person who was at the commencement of the Indian Income-tax (Amendment) Act, 1939, carrying on any business, profession or vocation on which tax was at any time charged under the provisions of the Indian Income-tax Act, 1918, is succeeded in such capacity by another person, the change not being merely a change in the constitution of a partnership, no tax shall be payable by the first mentioned person in respect of the income, profits and gains of the period between the end of the previous year and the date of such succession, and such person may further claim that the income, profits and gains of the previous year shall be deemed to have been the income, profits and gains of the said period.Where any such claim is made, an assessment shall be made on the basis of the income, profits and gains of the said period, and, if an amount of tax has already been paid in respect of the income, profits and gains of the previous year exceeding the amount payable on the basis of such assessment, a refund shall be given of the difference".5.7.Sections 26, 48 and 55 of the Act fully bear out this position.It was argued that a different firm was then constituted.8..
```

### CaseSummarizer

``` 
python preprocess.py sample folder sample_processed
python summary.py sample_processed sample_summary dictionary.txt
python summary_length.py sample_summary sample_shortsumm 0.34

But under the Income tax Act the position is somewhat different It appears that a fresh partnership deed was drawn up in the year 1945 when Gilbert was brought in The appeal therefore fails and is dismissed with costs In 1924 Mathews went out and his share was taken over by Figgies and Notley The Tribunal in spite of this document took the view that under the Partnership Act a firm could be carried on even if there was a change in its constitution The High Court refused to look into this document as it had not been relied upon before the Tribunal and no reference bad been specifically made to it in the order of the Income tax Officer or the Assistant Commissioner It is true that under the law of partnership a firm has no legal existence apart from its partners and it is merely a compendious name to describe its partners but it is also equally true that under that law there is no dissolution of the firm by the mere incoming or outgoing of partners Reference was made by Mr Daphtary to the partnership deed drawn up in 1 It was argued that a different firm was then constituted The true question to decide is one of identity of the unit assessed under the Income tax Act 1918 which paid double tax in the year 1939 with the unit to whose business the private limited company succeeded in the year 1 We have no doubt that the Tribunal and the High Court were right in holding that in spite of the mere changes in the constitution of the firm the business of the firm as originally constituted continued as tea brokers right from its inception till the time it was succeeded by the limited company and that it was the same unit all through carrying on the same business at the same place and there was no cesser of that business or any change in the unit The assessee is a partnership concern It upheld the view taken by the Tribunal A firm can be charged as a distinct assessable entity as distinct from its partners who can also be assessed individually Sections 26 48 and 55 of the Act fully bear out this position In 1939 Hillman was brought in and the partnership consisted of these three partners The Income tax Officer disallowed the claim of the assessee on the ground that the partners of the firm in 1939 being different from the partners of the firm in 1947 no relief could be given to the applicant Section 3 which is the charging section is in these terms Where any Central Act enacts that income tax shall be charged for any year at any rate or rates tax at that rate or those rates shall be charged for that year in accordance with and subject to the provisions of this Act in respect of the total income of the previous year of every individual Hindu undivided family company and local authority and of every firm and other association of persons or the partners of the firm or the members of the association individually The partners of the firm are distinct assessable entities while the firm as such is a separate and distinct unit for purposes of assessment The result is that we see no substantial grounds for disturbing the opinion given by the High Court on the question submitted to it The law with respect to retiring partners as enacted in the Partnership Act is to a certain extent a
```