try:
  invoker = await setup_commands(config_path)
  
  # Authentication
  username = Prompt.ask("Username")
  password = Prompt.ask("Password", password=True)
  
  try:
      token = await invoker.execute_command("auth", username, password)
      console.print(f"[green]Authentication successful![/green]")
  except Exception as e:
      console.print(f"[red]Authentication failed: {str(e)}[/red]")
      return

  # Interactive chat loop
  console.print("\n[yellow]Starting chat session (type 'exit' to quit)[/yellow]")
  while True:
      query = Prompt.ask("\nYou")
      if query.lower() == 'exit':
          break

      context = {}
      if Prompt.ask("Add context? [y/N]").lower() == 'y':
          while True:
              key = Prompt.ask("Context key (or enter to finish)")
              if not key:
                  break
              value = Prompt.ask("Context value")
              context[key] = value

      try:
          response = await invoker.execute_command("chat", query, context)
          console.print("\n[blue]Assistant:[/blue]")
          console.print(response["raw_response"])
          console.print(f"\n[dim]Tokens: {response['tokens']}[/dim]")
      except Exception as e:
          console.print(f"[red]Error: {str(e)}[/red]")

except Exception as e:
  console.print(f"[red]Error: {str(e)}[/red]")
