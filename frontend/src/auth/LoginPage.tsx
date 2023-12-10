import { Formik, Field, Form } from "formik";
import React, { useEffect } from "react";
import useLogin from "./useLogin";

function Styled(props: { children: React.ReactNode }) {
  return <div className="bg-stone-900">{props.children}</div>;
}

function Title() {
  return (
    <div className="text-3xl text-teal-950 justify-self-center font-light pb-8">
      Log in to Reviewed
    </div>
  );
}

function SubmitButton() {
  return (
    <div className="w-full grid p-8">
      <button
        type="submit"
        className="bg-teal-950 px-4 py-2 text-light justify-self-center text-white"
      >
        Submit
      </button>
    </div>
  );
}

export default function LoginPage() {
  const { onLoginSubmit, errorMessage } = useLogin();

  useEffect(() => {}, [errorMessage]);
  return (
    <div className="h-screen w-screen flex justify-center items-center bg-stone-100">
      <div className="flex-col grid items-center">
        <Title />
        <Formik
          initialValues={{
            email: "",
            password: "",
          }}
          onSubmit={onLoginSubmit}
        >
          <Form>
            <label htmlFor="email">Email</label>
            <Styled>
              <Field
                id="email"
                name="email"
                placeholder="your.name@pwr.edu.pl"
                type="email"
              />
            </Styled>

            <label htmlFor="password">Password</label>
            <Styled>
              <Field
                id="password"
                name="password"
                placeholder=""
                type="password"
              />
            </Styled>
            <div className="text-red-700 text-sm text-thin">{errorMessage}</div>
            <SubmitButton />
          </Form>
        </Formik>
      </div>
    </div>
  );
}
