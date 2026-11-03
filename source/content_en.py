#!/usr/bin/env python3
"""The SELYVO website's English words — every page, the shared parts, the SEO texts. The other 14 languages are translations of this
file's JSON (content/<lang>.json, same keys). usage: python3 content_en.py → content/en.json"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))

EN = {
  'lang': 'en', 'cc': 'GB', 'hreflang': 'en-GB', 'name': 'English',
  'common': {
    'site': 'SELYVO Market',
    'skip': 'Skip to content',
    'nav': {'buy': 'Buy', 'sell': 'Sell', 'orders': 'Orders', 'invoices': 'Invoices', 'projects': 'Projects', 'trust': 'Trust',
            'core': 'SELYVO Core', 'videos': 'Videos', 'join': 'How to join', 'signIn': 'Sign in', 'menu': 'Menu', 'language': 'Language',
            'home': 'Home'},
    'areas': {'buy': 'Buy', 'sell': 'Sell', 'orders': 'Orders & deliveries', 'invoices': 'Invoices & payments',
              'projects': 'Projects & MailChat', 'trust': 'Trust & compliance', 'core': 'SELYVO Core'},
    'readMore': 'Read more',
    'trail': {'label': 'One deal, one trail',
              'lede': 'Each document is made from the one before it, so nothing is typed twice and both sides see the same record.',
              'request': 'Request', 'offer': 'Offer', 'order': 'Order', 'invoice': 'Invoice',
              'requestNote': 'Panels and fittings, sent to five invited suppliers',
              'offerNote': '€8,469.60 from Holzwerk Brandt, 4.8% less after the negotiation',
              'orderNote': 'Accepted by the supplier, delivery by 13 November',
              'invoiceNote': 'Made from the order and matched to what was received'},
    'videos': {
      'eyebrow': 'Video guides', 'title': 'See it in action',
      'lede': 'Short guides filmed in the product itself, narrated and captioned in your language.',
      'enScreens': 'The screens in these videos are in English; the voice and the captions are in English.',
      'watch': 'Watch', 'watchVideo': 'Watch the video', 'more': 'All video guides', 'minutes': 'min',
      'overview': {'title': 'SELYVO Market at a glance', 'text': 'Feeds, the Store, purchases, sales, orders, invoices, projects and MailChat in one tour.'},
      'joining': {'title': 'Joining from an invitation', 'text': 'From the invitation e-mail to your first day on SELYVO, step by step.'},
      'buying': {'title': 'From an idea to an approved order', 'text': 'A request for proposal, the offers, an AI negotiation, the purchase order and the supplier’s approval.'},
      'freelancer': {'title': 'Time, expenses and the invoice', 'text': 'A freelancer’s time sheet, expenses read from receipts, and one invoice for both.'}},
    'join': {
      'eyebrow': 'Membership', 'title': 'Join by invitation',
      'text': 'SELYVO Market is open only to businesses invited by a member, so every company on it is known to at least one other. '
              'Ask a customer or a supplier who is already on SELYVO to invite you. The invitation e-mail takes you through registration.',
      'points': ['The invitation works once, for 14 days, and only for the e-mail address it was sent to.',
                 'Your company is found in its business register and checked against sanctions lists before it can trade.',
                 'SELYVO’s fees are paid from a prepaid budget as they fall due. You add funds by card or bank transfer.'],
      'write': 'Write to us', 'watch': 'Watch how joining works', 'signIn': 'Sign in'},
    'contact': {
      'eyebrow': 'Contact', 'title': 'Questions before you join?',
      'lede': 'Write to us about SELYVO Market, SELYVO Core or a partnership. We reply by e-mail.',
      'firstName': 'First name', 'lastName': 'Last name', 'company': 'Company', 'email': 'Work e-mail', 'country': 'Country',
      'topic': 'What it is about',
      'topics': ['Joining SELYVO Market', 'SELYVO Core for my organisation', 'A partnership', 'Something else'],
      'message': 'Your message', 'send': 'Send',
      'note': 'We use your details only to reply to you.', 'required': 'Fill in your name, your e-mail and your message.'},
    'faqTitle': 'Questions people ask',
    'related': 'Also on SELYVO',
    'coming': 'Coming next',
    'example': 'Example',
    'footer': {
      'about': 'SELYVO Market is a business marketplace for verified companies and freelancers: buy, sell, invoice and work together in one place.',
      'market': 'Market', 'company': 'SELYVO', 'contact': 'Contact', 'guides': 'Video guides',
      'rights': '© 2026 SELYVO. All rights reserved.', 'languages': 'Languages'},
  },
  'pages': {
    'index': {
      'title': 'SELYVO Market — the B2B marketplace for verified businesses',
      'description': 'An invitation-only B2B marketplace: requests and offers, orders, invoices with VAT by country, time sheets and expenses, with AI that reads your documents.',
      'hero': {'eyebrow': 'Invitation-only business marketplace',
               'title': 'Where verified businesses buy, sell and work together.',
               'lede': 'SELYVO Market brings customers and suppliers onto one platform, from the first request to the paid invoice. '
                       'Every member is found in its business register, checked and qualified before it trades.',
               'cta': 'How to join', 'cta2': 'Watch the tour', 'shot': 'Purchases on SELYVO Market: what waits for you, and every request, offer and negotiation.'},
      'trust': [['Found in its register', 'Company ID, address and VAT number come from the business register.'],
                ['Checked', 'Sanctions lists are checked before a business can trade.'],
                ['Qualified', 'Its answers to SELYVO’s questions, with proofs, give it a first rating.'],
                ['Reviewed', 'Customers’ reviews take over as orders are completed.']],
      'areas': {'eyebrow': 'The marketplace', 'title': 'One marketplace for the whole business',
                'lede': 'Each area works on its own and hands over to the next: a request becomes an offer, an order, a delivery and an invoice without retyping.',
                'buy': 'Requests for proposal, offers compared line by line and purchase orders, with an AI negotiator that asks you before anything is agreed.',
                'sell': 'Listings with member prices, requests from your categories, targeted offers and a pipeline from lead to won.',
                'orders': 'Every purchase and sales order with its status: accepted, delivered in parts, received, invoiced, paid.',
                'invoices': 'Invoices from orders with VAT by country, and invoices you receive read by AI from a file or by e-mail.',
                'projects': 'Time sheets for each customer, expenses with receipts, and a business mailbox with chat in one list.',
                'trust': 'Invited members, register data, sanctions checks, qualification, approvals and the history of every record.',
                'core': 'Your own workspace for suppliers, questionnaires, catalogues and approval flows, alongside the Market.'},
      'how': {'eyebrow': 'Getting started', 'title': 'How a business starts on SELYVO',
              'steps': [['Get invited', 'A customer or supplier who is a member invites you by e-mail.'],
                        ['Register your company', 'SELYVO finds it in the business register. You confirm it and say what you buy and sell.'],
                        ['Qualify', 'Answer SELYVO’s questions and any your inviter asks. Your first rating follows.'],
                        ['Trade', 'Publish listings, answer requests, send offers, take orders and invoice, all on SELYVO.']]},
      'ai': {'eyebrow': 'AI', 'title': 'AI that reads and drafts. You decide.',
             'lede': 'AI does the reading and the first draft. Nothing is sent, agreed or booked until a person says so.',
             'items': [['Reads your files', 'A specification becomes a request with lots and lines. A supplier’s PDF becomes an offer. A receipt becomes an expense.', ''],
                       ['Reads your mail', 'Invoices, offers and orders that arrive by e-mail are recognised and prepared for you.', ''],
                       ['Negotiates for you', 'An AI negotiator writes to the supplier in its language, within the position you set, and asks you before anything is agreed.', 'coming'],
                       ['Your choice of model', 'Your business picks the AI model it uses, from those SELYVO offers, and how hard it works. Each use is listed with its cost.', '']]},
      'audiences': {'eyebrow': 'Who it is for', 'title': 'Made for every side of a deal',
                    'items': [['For buyers', 'Publish requests, compare offers, order and pay, with suppliers you know are real.'],
                              ['For suppliers', 'Be found by verified buyers in your categories, answer their requests and get paid on your terms.'],
                              ['For freelancers', 'Keep time and expenses for each customer and invoice them in one go.']]},
      'core': {'eyebrow': 'For larger organisations', 'title': 'SELYVO Core: your own operating layer',
               'text': 'Need SELYVO’s processes inside your organisation? SELYVO Core adds supplier management, questionnaires, catalogues and approval flows with AI checks, alongside the Market and the systems you already run.',
               'link': 'Explore SELYVO Core'},
      'langs': {'title': 'In your language',
                'text': 'SELYVO Market speaks English, Czech, Slovak, German, Spanish, Danish and Swedish, and each person chooses their own. '
                        'Questionnaires are written in each language, and AI translates the missing ones. This website and its video guides are in 15 languages.'},
      'faq': [['Who can join SELYVO Market?', 'Businesses and freelancers invited by a member. Ask a customer or supplier who is on SELYVO to invite you. If you do not know anyone on SELYVO yet, write to us.'],
              ['How does SELYVO know a business is real?', 'Each company is found in its business register, checked against sanctions lists and qualified with SELYVO’s questions before it can trade. Customers’ reviews follow its orders.'],
              ['What does it cost?', 'SELYVO’s fees are paid from a prepaid budget as they fall due. You add funds by card or bank transfer and see every charge in your account.'],
              ['Does it work with our accounting?', 'Invoices carry VAT by country and the wording each case requires, and they print or save as PDF. Invoices made in your own accounting can be sent through SELYVO from a file.'],
              ['Is there a phone app?', 'SELYVO works in the browser on a computer, a tablet or a phone. Every screen adapts to a phone.']]},

    'spend-control': {
      'title': 'Buy on SELYVO Market — requests, offers and purchase orders',
      'description': 'Publish a request for proposal, typed or read by AI from a file. Compare offers by lot and line, negotiate and send purchase orders to verified suppliers.',
      'hero': {'eyebrow': 'Buy', 'title': 'From a need to an approved order, with suppliers you can trust.',
               'lede': 'Describe what you need, or drop the specification and let AI read it. Verified suppliers quote, you compare their offers line by line, '
                       'negotiate and place the order. Every step stays on record.',
               'shot': 'Compare offers by lot: Holzwerk Brandt’s €8,894.40 for panels and fittings beside Nordic Panels’ €9,138.60.'},
      'features': {'title': 'Everything a purchase needs', 'items': [
        ['Requests from a file', 'Drop a specification: AI finds the lots, the lines with quantities and units, and the questions for suppliers. Nothing is filled in before you check it.'],
        ['Lots for products and services', 'Put the materials in one lot and the transport or assembly in another. Each lot has its own budget and is awarded on its own.'],
        ['You choose who quotes', 'Any supplier in the category from the countries you pick, or only those you invite by name. Your questionnaires go with the request.'],
        ['Offers compared side by side', 'By lot, by offer or line by line: price, delivery and terms next to each other, with the lowest price and the earliest delivery marked.'],
        ['Purchase orders from the offer', 'Award each lot and create the purchase order from the winning offer. The supplier accepts it on SELYVO and you follow it to delivery and invoice.'],
        ['Everyday buying from the Store', 'For regular items, order straight from verified suppliers’ listings at member prices, or collect them in the basket.']]},
      'flow': {'title': 'A purchase, step by step', 'steps': [
        ['Request', 'Typed or read from a file, with lots, lines and questions.'],
        ['Offers', 'Suppliers quote by the deadline you set.'],
        ['Negotiation', 'Yourself, or with the AI negotiator.'],
        ['Award', 'The best offer for each lot.'],
        ['Order', 'Sent, accepted and followed to the invoice.']]},
      'highlight': {'title': 'The AI negotiator', 'badge': 'coming',
                    'text': 'Set what matters, your target and your limit. The AI writes to the supplier in its language from your SELYVO mailbox, says that it is an AI, '
                            'and asks you before anything is agreed. In the video it agrees €8,469.60 on an offer of €8,894.40, 4.8% less.'},
      'video': 'buying',
      'faq': [['Can a supplier that is not on SELYVO send an offer?', 'Invite it by e-mail with your request. It joins SELYVO before it can send an offer, so every offer comes from a verified business.'],
              ['Do suppliers see my budget?', 'No. A lot’s budget is for your own planning. Suppliers see it only if you choose to share it.'],
              ['Can I buy without a request?', 'Yes. Order straight from a listing in the Store, at the member price the supplier sets.']],
      'related': ['sell', 'orders', 'invoices']},

    'revenue-acceleration': {
      'title': 'Sell on SELYVO Market — listings, requests and targeted offers',
      'description': 'Reach verified buyers: list products and services at member prices, answer requests in your categories, send targeted offers and follow every sale to the win.',
      'hero': {'eyebrow': 'Sell', 'title': 'Be found by buyers who are ready to order.',
               'lede': 'List what you sell, answer the requests published in your categories and send offers to the customers you choose. '
                       'Your pipeline shows every case from the first lead to the win.',
               'shot': 'Sales on SELYVO Market: every case from lead to won, with its value at each stage.'},
      'features': {'title': 'Selling, end to end', 'items': [
        ['Listings with member prices', 'Products and services with photos, prices by quantity or package, delivery times and the regions you serve.'],
        ['Requests that fit you', 'Requests in your categories and regions reach you in Sales as opportunities. Answer with an offer, line by line.'],
        ['Targeted offers', 'Send an offer to the customers you choose. They see it in their feed and can order straight from it.'],
        ['Your pipeline', 'Every sales case from lead to won or lost, with its value at each stage and the next step.'],
        ['Feeds that work for you', 'Post updates for your customers and for businesses in your categories, and promote an update or a listing to reach more of them.'],
        ['Paid sooner', 'Invoice from the order with VAT by country. Or have SELYVO collect the invoice: SELYVO pays you, less its fee, and the customer pays SELYVO.']]},
      'flow': {'title': 'A sale, step by step', 'steps': [
        ['Listing', 'Your products and services, with member prices.'],
        ['Request', 'A buyer asks, in your category.'],
        ['Offer', 'Your answer, line by line.'],
        ['Order', 'Accepted and delivered.'],
        ['Invoice', 'Issued from the order and paid.']]},
      'video': 'overview',
      'faq': [['Who sees my listings?', 'Members of SELYVO Market, in the regions you deliver to. They see your member prices and your rating.'],
              ['Can I sell to a company that is not on SELYVO yet?', 'Invite it. Once it has joined, it can order from you and receive your invoices on SELYVO.'],
              ['How do requests reach me?', 'Requests published in your categories and countries appear in Sales. A buyer can also invite you by name.']],
      'related': ['buy', 'orders', 'invoices']},

    'inventory-control': {
      'title': 'Orders and deliveries on SELYVO Market',
      'description': 'Purchase and sales orders in one list: accepted, delivered in parts with delivery notes, received, invoiced and paid, with messages and documents on each order.',
      'hero': {'eyebrow': 'Orders & deliveries', 'title': 'Every order, from accepted to paid, in one place.',
               'lede': 'An order on SELYVO carries its own timeline. The supplier accepts and delivers, in parts if needed; the customer confirms what arrived; '
                       'the invoice follows. Both sides see the same record.',
               'shot': 'Order ORD-7311: accepted by Holzwerk Brandt, delivery by 13 November, and what happens next.'},
      'features': {'title': 'Orders both sides can rely on', 'items': [
        ['One status for both sides', 'Ordered, accepted, delivered, received, invoiced, paid: customer and supplier see the same steps and dates.'],
        ['Deliveries in parts', 'Each delivery has its delivery note. The customer confirms what arrived, and the rest stays open.'],
        ['Messages on the order', 'Talk about the order where it lives. Nothing is sent until you press Send.'],
        ['Documents linked together', 'The order, its delivery notes, the offer it came from and its invoices all point to each other.'],
        ['When something is wrong', 'Raise an issue on the order and keep the conversation and the evidence with it.'],
        ['Print or save as PDF', 'With your logo, for your records or your warehouse.']]},
      'flow': {'title': 'An order’s steps', 'steps': [
        ['Ordered', 'Sent from the offer or the Store.'],
        ['Accepted', 'The supplier confirms it.'],
        ['Delivered', 'With a delivery note, in parts if needed.'],
        ['Received', 'The customer confirms what arrived.'],
        ['Invoiced and paid', 'The invoice follows the order.']]},
      'video': 'buying',
      'faq': [['Can a supplier deliver in several parts?', 'Yes. Each part has its delivery note and the customer confirms what arrived. The order stays open until everything is in.'],
              ['Who can see an order’s messages?', 'The people working on the order at both businesses. A message goes out only when you press Send.'],
              ['Do orders follow approval rules?', 'Yes. Your business decides who approves which orders, and the order waits until they do.']],
      'related': ['buy', 'sell', 'invoices']},

    'finance-administration': {
      'title': 'Invoices, VAT and payments on SELYVO Market',
      'description': 'Invoice from orders with the right VAT for each country, receive invoices read by AI from a file or by e-mail, and see what is due and overdue in one list.',
      'hero': {'eyebrow': 'Invoices & payments', 'title': 'Invoices that check themselves against the order.',
               'lede': 'Issue invoices from your orders with VAT by country and the wording the law requires. Invoices you receive, by e-mail, as a file or on SELYVO, '
                       'are read by AI and matched to their order before you approve them.',
               'shot': 'Invoice FV-2026-0018 to Nordform ApS: the hours and the expenses of October, with the reverse charge.'},
      'features': {'title': 'Less retyping, fewer surprises', 'items': [
        ['VAT by country', 'The rate, the reverse charge or the exemption for the two countries, and the legal wording for each case.'],
        ['Invoices by e-mail', 'Suppliers send invoices to invoice@market.selyvo.com. AI reads each one, finds your business and the order, and asks the sender for anything missing.'],
        ['Invoices from a file', 'Drop a PDF and AI reads the supplier, the lines, the VAT and the totals for you to check.'],
        ['Without a purchase order, within your rules', 'Accept invoices without a purchase order from the suppliers you choose, up to the amount you set.'],
        ['Expenses with receipts', 'Receipts read by AI, billed on to a customer’s order or kept as your own cost.'],
        ['Payables, receivables, overdue', 'One list for both sides, with what is due and what is late.']]},
      'flow': {'title': 'An invoice you receive', 'steps': [
        ['Arrives', 'On SELYVO, by e-mail or as a file.'],
        ['Read by AI', 'Supplier, lines, VAT and totals.'],
        ['Matched', 'To its order and what was received.'],
        ['Approved', 'By whoever your rules name.'],
        ['Paid', 'And marked paid on both sides.']]},
      'video': 'freelancer',
      'faq': [['Can I send invoices made in my own accounting?', 'Yes. Upload the file: SELYVO reads it and sends it to the customer with its order.'],
              ['Can we bring our past invoices?', 'Yes. Your past invoices are read by AI, and their suppliers can be invited to SELYVO.'],
              ['How is VAT handled across borders?', 'SELYVO applies the rate, the reverse charge or the exemption that fits the two countries and prints the wording the law requires.']],
      'related': ['orders', 'projects', 'buy']},

    'operational-scale': {
      'title': 'Projects, time sheets, expenses and MailChat on SELYVO Market',
      'description': 'Time sheets a week at a time for each customer, expenses with receipts, one invoice for both, and e-mail and chat with partners in one business mailbox.',
      'hero': {'eyebrow': 'Projects & MailChat', 'title': 'Work for your customers without the paperwork.',
               'lede': 'Time sheets, expenses and messages live next to the orders they belong to. Customers approve what they want to approve, '
                       'and you invoice the rest in one go.',
               'shot': 'Your time in Projects: a week at a time for every customer, and what needs your attention.'},
      'features': {'title': 'Time and expenses, ready to invoice', 'items': [
        ['Your week, every customer', 'Enter hours or days for each customer and order, with what you did. The customer reads it on the time sheet.'],
        ['Each customer’s own rules', 'Approved before the invoice, attached to it, or not needed, weekly or monthly, as each customer decides.'],
        ['Expenses billed on', 'Book an expense with its receipt. It waits in the customer’s monthly charge until it is approved.'],
        ['One invoice for both', 'Approved hours and expenses go on one invoice, each expense without its VAT.'],
        ['Own time, kept apart', 'Pre-sales, bids and training are counted at internal rates and never reach a customer.'],
        ['MailChat', 'A business mailbox inside SELYVO: e-mails and chats with customers and suppliers in one list, with AI that recognises invoices, offers and orders.']]},
      'flow': {'title': 'From hours to invoice', 'steps': [
        ['Hours', 'Entered a week at a time.'],
        ['Time sheet', 'Sent for the customer’s period.'],
        ['Approval', 'By the customer, if it asks for one.'],
        ['Invoice', 'Hours and expenses together.']]},
      'highlight': {'title': 'Projects with budgets and milestones', 'badge': 'coming',
                    'text': 'Projects with a budget, milestones and tasks, with every purchase, sale, hour and expense counted against them.'},
      'video': 'freelancer',
      'faq': [['Can a customer approve time sheets on SELYVO?', 'Yes. The customer’s approver sees each time sheet with its days and what was done, and approves it or returns it with a comment.'],
              ['Do I need MailChat?', 'No, it is optional. It gives your business a SELYVO mailbox for writing to partners, and your own e-mail address is never shown.'],
              ['Can freelancers use SELYVO?', 'Yes. A freelancer joins as a one-person business, by invitation like any other, and works with the same tools.']],
      'related': ['invoices', 'sell', 'trust']},

    'compliance-by-design': {
      'title': 'Trust and compliance on SELYVO Market',
      'description': 'Members are invited, found in their business register, checked against sanctions lists and qualified before they trade. Every record keeps its history.',
      'hero': {'eyebrow': 'Trust & compliance', 'title': 'Know who you deal with, and keep proof of what was agreed.',
               'lede': 'Every business on SELYVO is invited by a member, found in its register, checked and qualified before it trades. '
                       'Every record keeps its history: who did what, and when.',
               'shot': 'Registration: the company found in its business register, confirmed with one click.'},
      'features': {'title': 'Trust built into every step', 'items': [
        ['Invited by a member', 'No anonymous sign-ups. Every business joins through an invitation from a customer or supplier who is already on SELYVO.'],
        ['Found in the register', 'Company ID, address, VAT number and registered activities come from the official business register.'],
        ['Sanctions checks', 'Each business is checked against sanctions lists when it joins, before it can trade.'],
        ['Qualification and questionnaires', 'SELYVO’s questions with proofs give a first rating. Your own questionnaires go to your suppliers and customers.'],
        ['Rights and approvals', 'Each person sees what their role allows. Your approval rules decide who approves orders, time sheets and expenses.'],
        ['A history for every record', 'Requests, offers, orders and invoices keep their history: who changed what, and when.']]},
      'flow': {'title': 'How a business is admitted', 'steps': [
        ['Invitation', 'From a member.'],
        ['Register', 'Company data from the business register.'],
        ['Checks', 'Sanctions lists.'],
        ['Qualification', 'Answers, proofs, a first rating.'],
        ['Reviews', 'From customers, order by order.']]},
      'video': 'joining',
      'faq': [['Can we set our own requirements for suppliers?', 'Yes. Send your own questionnaires with an invitation or a request, and see the answers and their proofs before you decide.'],
              ['Who sees what inside our business?', 'Each person sees what their role allows. Amounts and finances are shown only to people with the rights to see them.'],
              ['What does a partner see of us?', 'Only what you send or publish: your listings, your offers, your orders and invoices with them, and your profile.']],
      'related': ['buy', 'sell', 'core']},

    'operating-layer': {
      'title': 'SELYVO Core — the operating layer for your own processes',
      'description': 'For organisations with their own processes: supplier management, questionnaires, catalogues and approval flows with AI checks, alongside SELYVO Market.',
      'hero': {'eyebrow': 'SELYVO Core · optional', 'title': 'Your own processes, on the same foundation as the Market.',
               'lede': 'SELYVO Core gives larger organisations their own workspace: suppliers with risk and performance, questionnaires, catalogues and process flows '
                       'with AI checks, connected to SELYVO Market and to the systems you already run.',
               'shot': 'The suppliers board in SELYVO Core: active, preferred, high-risk and onboarding suppliers, and every request to add one.'},
      'features': {'title': 'What SELYVO Core adds', 'items': [
        ['Suppliers board', 'Active, preferred, high-risk and onboarding suppliers with the KPIs you choose, and every request to add a supplier in one queue.'],
        ['Questionnaires', 'Reusable question sets for onboarding, assessment and ESG, answered by suppliers with proofs and scored.'],
        ['Request & shop', 'A catalogue for employees with preferred items, bundles and budgets per cost centre. Requests flow into approval.'],
        ['Processes with AI checks', 'Approval flows in which an AI check screens a supplier or a document and returns pass, fail or needs review. A person decides.'],
        ['Fits your landscape', 'Run it as integrated SELYVO modules, or as one harmonised interface over the ERP, CRM and procurement systems you keep.'],
        ['Configured, not coded', 'Every limit and threshold is set by your operators. Nothing is written into the code.']]},
      'flow': {'title': 'One operating model', 'steps': [
        ['Capture', 'Requests, documents and data come in once.'],
        ['Understand', 'AI reads, checks and classifies them.'],
        ['Execute', 'Processes route the work.'],
        ['Control', 'Approvals and rules keep it in bounds.'],
        ['Improve', 'KPIs show where to act.']]},
      'shots': ['The suppliers board, with the KPIs you choose.', 'Questionnaires for onboarding, assessment and ESG.',
                'Request & shop: the catalogue for employees.', 'A process with an AI check as an approval step.'],
      'faq': [['Do we need SELYVO Core to use the Market?', 'No. SELYVO Market works on its own. Core is for organisations that want their own processes and workspace.'],
              ['Can Core run alongside our ERP?', 'Yes. It can be the system where the work happens, or one interface over the systems you keep.'],
              ['How do we start?', 'With one process, such as supplier onboarding or employee purchasing, measured before and after.']],
      'related': ['buy', 'trust', 'invoices']},

    'thank-you': {
      'title': 'Thank you — SELYVO',
      'description': 'Thank you for your message to SELYVO.',
      'hero': {'eyebrow': 'Message sent', 'title': 'Thank you. We have your message.',
               'lede': 'We will reply by e-mail. Meanwhile, watch the video guides or read how joining works.'},
      'links': {'videos': 'Watch the video guides', 'join': 'How to join', 'home': 'Back to the home page'}},
  },
}

if __name__ == '__main__':
    os.makedirs(os.path.join(D, 'content'), exist_ok=True)
    json.dump(EN, open(os.path.join(D, 'content', 'en.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    n = len(json.dumps(EN, ensure_ascii=False).split())
    print('content/en.json', n, 'words (about)')
