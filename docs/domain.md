# Setting Up adskticket.com with AWS Route 53 and Load Balancer

## 1. Purchase Domain

- Buy the domain `adskticket.com` from your preferred domain registrar (e.g., Namecheap, GoDaddy, Google Domains).

## 2. Create a Hosted Zone in Route 53

- Go to the [AWS Route 53 Console](https://console.aws.amazon.com/route53/).
- Click **"Hosted zones"** > **"Create hosted zone"**.
- Enter `adskticket.com` as the domain name.
- Choose **Public hosted zone**.
- Click **Create hosted zone**.

## 3. Update Domain Registrar with AWS Nameservers

- In the Route 53 hosted zone details, copy the four **NS (Name Server)** records.
- Go to your domain registrar’s dashboard.
- Find the DNS or Nameserver settings for `adskticket.com`.
- Replace the default nameservers with the four AWS Route 53 nameservers.
- Save changes. (It may take a few minutes to a few hours for DNS propagation.)

## 4. Create a Record for the Load Balancer

- In the Route 53 hosted zone for `adskticket.com`, click **"Create record"**.
- Choose **Record type:**  
  - If using an AWS Application Load Balancer (ALB), select **A – Routes traffic to an IPv4 address and some AWS resources**.
  - Choose **Alias** and select your ALB from the dropdown.
- For **Record name**, leave blank to use the root domain (`adskticket.com`), or enter a subdomain (e.g., `www`).
- Click **Create records**.

## 5. Verification

- After DNS propagation, visiting `https://adskticket.com` should route traffic to your AWS Load Balancer and, in turn, your application.

---

**Summary:**  
You purchased `adskticket.com`, pointed its nameservers to AWS Route 53, and created an alias record in Route 53 to route traffic from your domain to your AWS Load Balancer.
Collapse

















